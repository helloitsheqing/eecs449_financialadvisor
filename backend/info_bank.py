# from app import app
from database import get_db
from flask import Blueprint
import flask
import json
from datetime import datetime, timezone
import pdbp
from chatbot import get_chatbot_response

info_bank = Blueprint('info_bank', __name__)

@info_bank.route("/info_bank/<string:username>/clear-chats", methods=["DELETE"])
def clear_chats(username):
    """Clear all chats from db."""

    # breakpoint()
    # username = flask.session.get("username")
    if username:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            DELETE FROM user_conversations WHERE username = ?
            """, (username,))
            conn.commit()
            return flask.jsonify({"success": True}), 200
    else:
        return flask.jsonify({"success": False, "message": "Unauthorized"}), 401


@info_bank.route("/info_bank/<string:username>/chats", methods=["GET"])
def see_chats(username):
    """See all chats in db."""

    # username = flask.session.get("username")

    if not username:
        return flask.jsonify({"success": False, "message": "Unauthorized"}), 401
    
    # breakpoint()
    try:
        with get_db() as conn:
            conversations = [
                dict(row) for row in conn.execute(
                    """
                    SELECT *
                    FROM user_conversations 
                    WHERE username = ?
                    ORDER BY created_at DESC
                    """, 
                    (username,)
                ).fetchall()
            ]

            for conv in conversations:
                conv["conversation_data"] = json.loads(conv["conversation_data"])

            return flask.jsonify({"success": True, "data": conversations}), 200
        
    except Exception as e:
        return flask.jsonify({"success": False, "message": f"Error fetching chats: {str(e)}"}), 500
    

@info_bank.route("/info_bank/<string:username>/chat/<string:chat_id>", methods=["GET", "POST"])
def see_chat_with_chat_id(username, chat_id):
    """See chat specified by chat_id."""

    # username = flask.session.get("username")
    # breakpoint()
    if username:
        with get_db() as conn:
            cursor = conn.cursor()

            if flask.request.method == "GET":
                cursor.execute("""
                SELECT * FROM user_conversations WHERE username = ? AND id = ? 
                """, (username, chat_id))  # this query might be redundant as every id is unique and has one username
                # lowkey just looking for an excuse to keep the username in the query as a sanity check

                conversation = dict(cursor.fetchone())
                conversation["conversation_data"] = json.loads(conversation["conversation_data"])
                if conversation:
                    return flask.jsonify({"success": True,
                                          "data": conversation}), 200  # might have to manually add elements from conversation to this dict
                else:
                    return flask.jsonify({"success": False,
                                          "message": "Conversation not found"}), 404
                
            elif flask.request.method == "POST":
                # breakpoint()
                cursor.execute("SELECT conversation_data FROM user_conversations WHERE username = ? AND id = ?", 
                               (username, chat_id))  # same thing here
                conversation = dict(cursor.fetchone())
                if conversation:
                    # breakpoint()
                    conversation = json.loads(conversation["conversation_data"])  # this turns the text into a list
                    user_prompt = flask.request.get_json().get('message')
                    bot_response = get_chatbot_response(user_prompt)
                    conversation.append({"prompt": user_prompt, "response": bot_response})
                    conversation = json.dumps(conversation)

                    cursor.execute("UPDATE user_conversations SET conversation_data = ?, updated_at = ? WHERE id = ?",
                                   (conversation, datetime.now(timezone.utc), chat_id))
                    conn.commit()
                    return flask.jsonify({"success": True,
                                          "message": "Prompt and response added to conversation",
                                          "response": bot_response}), 201
                else:
                    return flask.jsonify({"success": False,
                                          "message": "Conversation not found",
                                          "response": None}), 404
    else:
        return flask.jsonify({"success": False, "message": "Unauthorized"}), 401
