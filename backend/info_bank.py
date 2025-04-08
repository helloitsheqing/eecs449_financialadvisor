from app import app
from database import get_db
import flask
import json
import datetime
import pdbp

@app.route("/clear-chats", methods=["DELETE"])
def clear_chats():
    """Clear all chats from db."""

    # breakpoint()
    username = flask.session.get("username")
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


@app.route("/chats", methods=["GET"])
def see_chats():
    """See all chats in db."""

    username = flask.session.get("username")
    if username:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT * FROM user_conversations WHERE username = ?
            """, (username,))

            conversations = cursor.fetchall()
            return flask.jsonify({"success": True, "data": conversations}), 200
    else:
        return flask.jsonify({"success": False, "message": "Unauthorized"}), 400
        

@app.route("/chat/<int:chat_id>", methods=["GET", "POST"])
def see_chat_with_chat_id(chat_id):
    """See chat specified by chat_id."""

    username = flask.sessoion.get("username")

    if username:
        with get_db() as conn:
            cursor = conn.cursor()

            if flask.request.method == "GET":
                cursor.execute("""
                SELECT * FROM user_conversations WHERE username = ? AND id = ? 
                """, (username, chat_id))  # this query might be redundant as every id is unique and has one username
                # lowkey just looking for an excuse to keep the username in the query as a sanity check

                conversation = conn.fetchone()
                if conversation:
                    return flask.jsonify({"success": True, "data": conversation}), 200  # might have to manually add elements from conversation to this dict
                else:
                    return flask.jsonify({"success": False, "message": "Conversation not found"}), 404
                
            elif flask.request.method == "POST":
                cursor.execute("SELECT conversation_data FROM user_conversations WHERE username = ? AND id = ?", 
                               (username, chat_id))  # same thing here
                conversation = conn.fetchone()
                if conversation:
                    conversation = json.loads(conversation)  # this turns the text into a list

                    # TODO: implement form in frontend to exctract user_prompt and bot_response
                    user_prompt = ""
                    bot_response = ""
                    conversation.append({"prompt": user_prompt, "response": bot_response})
                    conversation = json.dumps(conversation)

                    cursor.execute("UPDATE user_conversations SET conversation_data = ?, updated_at = ? WHERE id = ?",
                                   (conversation, datetime.now(), chat_id))
                    conn.commit()
                    return flask.jsonify({"success": True,
                                          "message": "Prompt and response added to conversation"}), 201
                else:
                    return flask.jsonify({"success": False,
                                          "message": "Conversation not found"}), 404
    else:
        return flask.jsonify({"success": False, "message": "Unauthorized"}), 401