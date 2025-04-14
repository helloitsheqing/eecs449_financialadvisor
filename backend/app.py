from datetime import datetime, timedelta, timezone
from flask import Flask, request, jsonify, redirect, url_for, render_template
from flask_cors import CORS
import os
import json
import uuid
import flask
from dotenv import load_dotenv
from chatbot import get_chatbot_response, generate_conversation_title, change_model_bp
from auth import auth_bp, _build_preflight_response
from info_bank import info_bank
from excel import upload_excel_bp
from database import *
from flask_session import Session
from threading import Thread


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
CORS(
    app,
    supports_credentials=True,
    resources={r"/.*": {"origins": "*"}},
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type"],
    expose_headers=["Content-Type"]
)

app.register_blueprint(auth_bp)
app.register_blueprint(info_bank)
app.register_blueprint(upload_excel_bp)
app.register_blueprint(change_model_bp)


# Assign a unique session_id to each user on first visit
@app.before_request
def assign_session_id():
    if 'session_id' not in flask.session:
        flask.session['session_id'] = str(uuid.uuid4())
        flask.session.modified = True

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


# Chat route using session-based memory
@app.route('/chat/<string:username>', methods=['POST'])
def chat(username):
    """Handle new conversation logic."""
    # breakpoint()
    try:
        user_input = request.get_json().get('message')
        conversation_id = str(uuid.uuid4())
        final_response = get_chatbot_response(user_input, conversation_id)
        conversation_thread = Thread(target=save_conversation, args=(username,
            conversation_id,
            user_input,
            final_response))
        
        conversation_thread.start()
        conversation_thread.join()  # this makes things slightly better, but might actually just be redundant
        
        return jsonify({
            "response": final_response,
            "conversation_id": conversation_id
        })

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
                             (json.dumps(messages), datetime.now(timezone.utc), conversation_id))
            else:
                conversation_title = generate_conversation_title(prompt, response, conversation_id)  # this is breaking
                # conversation_title = "New Conversation"
                conn.execute("INSERT INTO user_conversations (id, username, conversation_title, conversation_data) VALUES (?, ?, ?, ?)",
                             (conversation_id, username, conversation_title,  # title will be changed later
                              json.dumps([{"prompt": prompt, "response": response}])))
            conn.commit()
    except Exception as e:
        print(f"Failed to save conversation: {e}")


# Run the app
if __name__ == '__main__':
    init_db()
    # train_model(model)
    app.run(port=5001, debug=True, host='0.0.0.0')
