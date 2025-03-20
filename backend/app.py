from flask import Flask, request, jsonify, redirect, url_for, render_template, session
from flask_cors import CORS
import requests
import os
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

from langchain import hub
from langchain_ollama import OllamaLLM
from langchain.tools import Tool
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.runnables.history import RunnableWithMessageHistory

import pdbp

# Not using LangSmith: Suppress warnings
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message="API key must be provided when using hosted LangSmith API")


# Load environment variables for API Keys
load_dotenv('backend_env.env')

app = Flask(__name__)
CORS(app) # Make sure to enable CORS!
app.secret_key = os.getenv('SECRET_KEY')

# Ollama API endpoint
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Model for Agent
AGENT_MODEL = "deepseek-r1:1.5b"

ALLOWED_CALLBACK_URL = "http://localhost:5001/callback"
ALLOWED_LOGOUT_URL = "http://localhost:5001"


# Auth0 configuration
oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=os.environ.get("AUTH0_CLIENT_ID"),
    client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{os.environ.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
    api_base_url=f"https://{os.getenv('AUTH0_DOMAIN')}",
    access_token_url=f"https://{os.getenv('AUTH0_DOMAIN')}/oauth/token",
    authorize_url=f"https://{os.getenv('AUTH0_DOMAIN')}/authorize",
)

# testing
@app.route('/test-session')
def test_session():
    session['test'] = 'This is a test'
    return session.get('test', 'Session not working')


# home
@app.route('/')
def home():
    # breakpoint()
    return render_template('home.html', session=session.get('user'))


# login
@app.route('/login')
def login():
    session.clear()
    return oauth.auth0.authorize_redirect(redirect_uri=os.getenv('AUTH0_CALLBACK_URL'))


# callback
@app.route('/callback')
def callback():
    # breakpoint()
    token = oauth.auth0.authorize_access_token(redirect_uri="http://localhost:5001/callback")  # this is failing
    # userinfo = oauth.auth0.get('userinfo').json()
    session['user'] = token
    return redirect('/')

# logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(
        f"https://{os.getenv('AUTH0_DOMAIN')}/v2/logout?"
        f"client_id={os.getenv('AUTH0_CLIENT_ID')}&"
        f"returnTo={url_for('home', _external=True)}"
    )


# Function Wrappers for external APIs
def get_stock_price(symbol: str) -> str:
    """ Fetch the current price of a stock using a financial API. """
    
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")  # Use environment variable for API key
    url = "https://www.alphavantage.co/query"
    
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": api_key
    }
    
    # Make API call and get response
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["Global Quote"]["05. price"]
    else:
        return "Error fetching stock price."


# Create Langchain tools for external APIs to be fed into the Agent 
api_tools = [
    Tool(
        name="GetStockPrice",
        func=get_stock_price,
        description="To fetch price for a particular stock."
    )
]


# Initialise Ollama LLM and add memory to the Agent
llm = OllamaLLM(model=AGENT_MODEL)
memory = ChatMessageHistory(session_id="test-session")
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm, api_tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=api_tools)
agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)


@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.get_json().get('message')
        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        # Use the agent to generate a response
        response = agent_with_chat_history.invoke({"input": user_input})
        return jsonify({"response": response})

    except Exception as e:
        # Handle any unexpected errors
        return jsonify({"error": str(e)}), 500


# Run the Flask app
if __name__ == '__main__':
    app.run(port=5001, debug=True, host='0.0.0.0')