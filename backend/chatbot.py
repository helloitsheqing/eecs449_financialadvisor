import requests
import flask
import os
from flask import jsonify
import re
from langchain import hub
from langchain_ollama import OllamaLLM
from langchain.tools import Tool
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.prompts import PromptTemplate

import warnings
warnings.filterwarnings("ignore", category=UserWarning, message="API key must be provided when using hosted LangSmith API")


AGENT_MODEL = "deepseek-r1:1.5b"
# AGENT_MODEL = "deepseek-r1:7b"  # DO NOT RUN THIS

def extract_output(input_text: str):
    """ Function to extract output after <think></think> tags from Agent's output response. """
    match = re.search(r"</think>(.*)", input_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return input_text.strip()


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


example_prompt = """You are a professional, reliable financial advisor. Answer clearly, concisely, and factually. Follow the tone and format of the examples below.

Example 1:
Q: How much should I have saved by age 30?
A: A common guideline is to have about one year's salary saved by age 30. This includes retirement accounts like 401(k)s or IRAs. Your target may vary depending on lifestyle, career, and financial goals.

Example 2:
Q: What's the difference between a Roth IRA and a Traditional IRA?
A: A Roth IRA is funded with after-tax dollars and grows tax-free, while a Traditional IRA is funded with pre-tax dollars and is taxed upon withdrawal. Roth is better if you expect to be in a higher tax bracket later.

Example 3:
Q: What is an emergency fund and how much do I need?
A: An emergency fund is money set aside for unexpected expenses. A good target is 3–6 months of living expenses in a liquid, easily accessible account.

Now answer the user's question below in the same tone and style.

Q: {input}
A:"""

# prompt = PromptTemplate(input_variables=["input"], template=example_prompt)
# prompt = hub.pull("hwchase17/react")
llm = OllamaLLM(model=AGENT_MODEL)

def get_financial_prompt():
    few_shot_examples = """You are a professional, reliable financial advisor. Answer clearly, concisely, and factually. Follow the tone and format of the examples below.

                        Example 1:
                        Q: How much should I have saved by age 30?
                        A: A common guideline is to have about one year's salary saved by age 30. This includes retirement accounts like 401(k)s or IRAs. Your target may vary depending on lifestyle, career, and financial goals.

                        Example 2:
                        Q: What's the difference between a Roth IRA and a Traditional IRA?
                        A: A Roth IRA is funded with after-tax dollars and grows tax-free, while a Traditional IRA is funded with pre-tax dollars and is taxed upon withdrawal. Roth is better if you expect to be in a higher tax bracket later.

                        Example 3:
                        Q: What is an emergency fund and how much do I need?
                        A: An emergency fund is money set aside for unexpected expenses. A good target is 3–6 months of living expenses in a liquid, easily accessible account.

                        Now answer the user's question below in the same tone and style.
                        """
    
    base_prompt = hub.pull("hwchase17/react")
    return base_prompt.partial(prefix=few_shot_examples)

prompt = get_financial_prompt()

def get_chatbot_response(user_input, conversation_id):
    # breakpoint()
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Create memory specific to user's session
    memory = ChatMessageHistory(session_id=conversation_id)  # TODO: look at incorporating memory?

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
        input_messages_key="input",  # conversation_id?
        history_messages_key="chat_history"
    )

    # Invoke the agent
    raw_response = agent_with_chat_history.invoke({"input": user_input}, {'configurable': {'session_id': conversation_id}})
    final_response = extract_output(raw_response.get("output", ""))

    return final_response


def generate_conversation_title(user_input, bot_response, conversation_id):
    agent = create_react_agent(llm=llm, tools=api_tools, prompt=prompt) # tools: api_tools
    agent_executor = AgentExecutor(agent=agent, 
                            tools=api_tools, 
                            handle_parsing_errors=True,
                            max_iterations=20, # Increased number of max iterations to avoid time out
                            max_execution_time=120) # Increased the maximum timeout to allow for longer processing) 

    agent_with_chat_history = RunnableWithMessageHistory(
        agent_executor,
        lambda session_id: ChatMessageHistory(session_id=session_id),
        input_messages_key="input",  # conversation_id?
        history_messages_key="chat_history"
    )

    raw_response = agent_with_chat_history.invoke({"input": f"""
                                                            Generate a short title for the following conversation:\n
                                                            Q: {user_input}\n
                                                            A: {bot_response}
                                                            """},
                                                  {'configurable': {'session_id': conversation_id}})  # ??????????????
    final_response = extract_output(raw_response.get("output", ""))
    return final_response
