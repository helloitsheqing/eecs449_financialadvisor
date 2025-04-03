from flask import Flask, request, jsonify, redirect, url_for, render_template, session
from flask_cors import CORS
import requests
import os
import json
import uuid
from dotenv import load_dotenv

from langchain import hub
from langchain_ollama import OllamaLLM
from langchain.tools import Tool
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
from auth import auth_bp
from database import *
from flask import Response, stream_with_context

# Suppress LangSmith warning
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message="API key must be provided when using hosted LangSmith API")

# Load environment variables
load_dotenv('backend_env.env')

app = Flask(__name__)
CORS(app, supports_credentials=True)
# More specific alternative if needed:
# CORS(app, resources={
#     r"/auth/*": {
#         "origins": ["http://localhost:3000"],
#         "methods": ["POST", "OPTIONS"],
#         "allow_headers": ["Content-Type"]
#     }
# })


# app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(auth_bp)



# @app.after_request
# def after_request(response):
#     # These headers will override the CORS configuration
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', '*')
#     response.headers.add('Access-Control-Allow-Methods', '*')
#     return response


# from auth import auth_routes
# app.register_blueprint(auth_routes)


app.secret_key = os.getenv('SECRET_KEY', default=uuid.uuid4().hex)

# Assign a unique session_id to each user on first visit
@app.before_request
def assign_session_id():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())

# Ollama model to use
AGENT_MODEL = "deepseek-r1:1.5b"
# AGENT_MODEL = "llama2"

# Homepage
@app.route('/')
def home():
    return render_template('home.html',
                           session=session.get('session_id'),
                           pretty=json.dumps(dict(session), indent=4))

# Clear session on logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Test session route
@app.route('/test-session')
def test_session():
    session['test'] = 'This is a test'
    print("session: ", session)
    return session.get('test', 'Session not working')

# # External API tool: Stock price lookup
# def get_stock_price(symbol: str) -> str:
#     api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
#     url = "https://www.alphavantage.co/query"
#     params = {
#         "function": "GLOBAL_QUOTE",
#         "symbol": symbol,
#         "apikey": api_key
#     }
#     response = requests.get(url, params=params)
#     if response.status_code == 200:
#         data = response.json()
#         try:
#             return data["Global Quote"]["05. price"]
#         except KeyError:
#             return "Stock data unavailable."
#     else:
#         return "Error fetching stock price."

# # LangChain tool wrapper
# api_tools = [
#     Tool(
#         name="GetStockPrice",
#         func=get_stock_price,
#         description="Fetches the current price for a given stock symbol."
#     )
# ]

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
@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.get_json().get('message')
        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        # Create memory specific to user's session
        memory = ChatMessageHistory(session_id=session['session_id'])

        # Create agent and executor fresh each time (ensures separation per request)
        agent = create_react_agent(llm=llm, tools=[], prompt=prompt) # tools: api_tools
        agent_executor = AgentExecutor(agent=agent, tools=[], handle_parsing_errors=True) # tools: api_tools
        agent_with_chat_history = RunnableWithMessageHistory(
            agent_executor,
            lambda _: memory,
            input_messages_key="input",
            history_messages_key="chat_history",
            max_iterations="10"
        )

        # Invoke the agent
        raw_response = agent_with_chat_history.invoke({"input": user_input}, {'configurable': {'session_id': session["session_id"]}})
        final_response = extract_output(raw_response.get("output", ""))
        return jsonify({"response": final_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        

# Run the app
if __name__ == '__main__':
    init_db()
    app.run(port=5001, debug=True, host='0.0.0.0')
