from datetime import timedelta
from flask import Flask, request, jsonify, redirect, url_for, render_template
from flask_cors import CORS
import requests
import os
import json
import uuid
import datetime
import flask
from dotenv import load_dotenv

from langchain import hub
from langchain_ollama import OllamaLLM
from langchain.tools import Tool
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
from auth import auth_bp, _build_preflight_response
from info_bank import info_bank
from excel import upload_excel_bp
from database import *
from flask import Response, stream_with_context
from flask_session import Session
from threading import Thread

# Suppress LangSmith warning
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message="API key must be provided when using hosted LangSmith API")

# Load environment variables
load_dotenv('backend_env.env')

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY', 'your-very-secret-key-here'),
    SESSION_TYPE='filesystem',  # Stores sessions on server
    SESSION_FILE_DIR='./flask_session',  # Directory for session files
    SESSION_COOKIE_NAME='laughing_stocks_session',
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,  # True in production
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(days=7)
)

Session(app)
# CORS(app,
#     supports_credentials=True,
#     resources={
#         r"/auth/*": {
#             "origins": "http://localhost:3000",
#             "methods": ["GET", "POST", "OPTIONS", "DELETE"],
#             "allow_headers": ["Content-Type"],
#             "expose_headers": ["Content-Type"],
#             "supports_credentials": True
#         },
#         r"/chat": {
#             "origins": "http://localhost:3000",
#             "methods": ["GET", "POST", "OPTIONS", "DELETE"],
#             "allow_headers": ["Content-Type"],
#             "expose_headers": ["Content-Type"],
#             "supports_credentials": True
#         },
#         r"/info_bank/*":{
#             "origins": "http://localhost:3000",
#             "methods": ["GET", "POST", "OPTIONS", "DELETE"],
#             "allow_headers": ["Content-Type"],
#             "expose_headers": ["Content-Type"],
#             "supports_credentials": True
#         }
#     })
CORS(
    app,
    supports_credentials=True,
    resources={r"/*": {"origins": "*"}},
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type"],
    expose_headers=["Content-Type"]
)
# CORS(app, resources={r"/*": {"origins": "*"}})

# app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(auth_bp)
app.register_blueprint(info_bank)
app.register_blueprint(upload_excel_bp)


# @app.after_request
# def after_request(response):
#     # These headers will override the CORS configuration
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', '*')
#     response.headers.add('Access-Control-Allow-Methods', '*')
#     return response
    


# from auth import auth_routes
# app.register_blueprint(auth_routes)


# Assign a unique session_id to each user on first visit
@app.before_request
def assign_session_id():
    if 'session_id' not in flask.session:
        flask.session['session_id'] = str(uuid.uuid4())
    
    # if "username" not in session:
    #     session['username'] = "username"
        # session['test'] = ""
    # session.permanent = True
    flask.session.modified = True

# Ollama model to use
AGENT_MODEL = "deepseek-r1:1.5b"
# AGENT_MODEL = "llama2"

# Homepage
@app.route('/')
def home():
    return render_template('home.html',
                           session=flask.session.get('session_id'),
                           pretty=json.dumps(dict(flask.session), indent=4))


# Test session route
@app.route('/test-session')
def test_session():
    flask.session['test'] = 'This is a test'
    flask.session.modified = True
    print("session: ", flask.session)
    print("username: ", flask.session.get("username"))
    print("app: ", app)
    # print("session username: ")
    return flask.session.get('test', 'Session not working')

# External API tool: Stock price lookup
def get_stock_price(symbol: str) -> str:
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        try:
            return data["Global Quote"]["05. price"]
        except KeyError:
            return "Stock data unavailable."
    else:
        return "Error fetching stock price."

# LangChain tool wrapper
api_tools = [
    Tool(
        name="GetStockPrice",
        func=get_stock_price,
        description="Fetches the current price for a given stock symbol."
    )
]

# Remove <think></think> tags from Agent's response
import re
def extract_output(input_text: str):
    """ Function to extract output after <think></think> tags from Agent's output response. """
    match = re.search(r"</think>(.*)", input_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return input_text.strip()


# Load prompt and LLM
prompt = hub.pull("hwchase17/react")
llm = OllamaLLM(model=AGENT_MODEL)

# Chat route using session-based memory
@app.route('/chat/<string:username>', methods=['POST'])
def chat(username):
    # breakpoint()
    try:
        user_input = request.get_json().get('message')
        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        # Create memory specific to user's session
        memory = ChatMessageHistory(session_id=flask.session['session_id'])  # TODO: look at incorporating memory?

        # Create agent and executor fresh each time (ensures separation per request)
        agent = create_react_agent(llm=llm, tools=api_tools, prompt=prompt) # tools: api_tools
        agent_executor = AgentExecutor(agent=agent, 
                                tools=api_tools, 
                                handle_parsing_errors=True,
                                max_iterations=20, # Increased number of max iterations to avoid time out
                                max_execution_time=120) # Increased the maximum timeout to allow for longer processing) 

        agent_with_chat_history = RunnableWithMessageHistory(
            agent_executor,
            lambda session_id: ChatMessageHistory(session_id=session_id),
            input_messages_key="input",
            history_messages_key="chat_history"
        )

        # Invoke the agent
        raw_response = agent_with_chat_history.invoke({"input": user_input}, {'configurable': {'session_id': flask.session["session_id"]}})
        final_response = extract_output(raw_response.get("output", ""))
        # breakpoint()
        if "conversation_id" not in flask.session:
            flask.session["conversation_id"] = str(uuid.uuid4())
            conversation_id = flask.session["conversation_id"]
            # username = flask.session.get("username")
            flask.session.modified = True
            # breakpoint()
        Thread(target=save_conversation, args=(username,
                conversation_id,
                user_input,
                final_response)).start()
        return jsonify({"response": final_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

def save_conversation(username, conversation_id, prompt, response):
    # breakpoint()
    try:
        with get_db() as conn:
            existing = conn.execute("SELECT conversation_data FROM user_conversations WHERE id = ?",
                                    (conversation_id,)).fetchone()
            if existing:
                messages = json.loads(existing["conversation_data"])
                messages.append({"prompt": prompt, "response": response})
                conn.execute("UPDATE user_conversations SET conversation_data = ?, updated_at = ? WHERE id = ?",
                             (json.dumps(messages), datetime.now(), conversation_id))
            else:
                conn.execute("INSERT INTO user_conversations (id, username, conversation_title, conversation_data) VALUES (?, ?, ?, ?)",
                             (conversation_id, username, "New Conversation",  # title will be changed later
                              json.dumps([{"prompt": prompt, "response": response}])))
            conn.commit()
    except Exception as e:
        print(f"Failed to save conversation: {e}")
        

# Run the app
if __name__ == '__main__':
    init_db()
    app.run(port=5001, debug=True, host='0.0.0.0')
