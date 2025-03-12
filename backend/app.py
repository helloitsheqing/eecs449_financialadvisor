from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from langchain_ollama import OllamaLLM

app = Flask(__name__)
CORS(app) # make sure to enable CORS!!

# Ollama API endpoint
OLLAMA_API_URL = "http://localhost:11434/api/generate"

@app.route('/chat', methods=['POST'])
def chat():
    print('1')
    user_input = request.get_json()['message']
    print(user_input)
    print('2')
    if not user_input:
        print('error no user input')

        return jsonify({"error": "No message provided"}), 400

    # print('3')
    # payload = {
    #     "model": "deepseek-r1:1.5b",
    #     "prompt": user_input,
    #     "stream": False  # (true if we want streaing responses)
    # }
    # print('4')
    # response = requests.post(OLLAMA_API_URL, json=payload)
    # print('5')
    #
    # if response.status_code != 200:
    #     return jsonify({"error": "Failed to get response from Ollama"}), 500
    #
    # ollama_response = response.json()
    # return jsonify({"response": ollama_response.get("response")})

    model = OllamaLLM(model='deepseek-r1:1.5b')
    result = model.invoke(input=user_input)
    return jsonify({"response": result})


if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')
