from app import app
from database import get_db
import flask
import pdbp

@app.route("/clear-chats", methods=["DELETE"])
def clear_chats():
    """Clear all chats from db."""

    # TODO: ensure session is persisting

    # breakpoint()
    username = flask.session.get("username")
    if username:
        with get_db() as conn:
            conn.execute("""
            DELETE * FROM user_conversations WHERE username = ?
            """, (username,))
            conn.commit()
            return flask.jsonify({"success": True}), 201
    else:
        return flask.jsonify({"success": False, "message": "Unauthorized"}), 400


@app.route("/chats", methods=["GET"])
def see_chats():
    """See all chats in db."""

    username = flask.session.get("username")
    if username:
        with get_db() as conn:
            conn.execute("""
            SELECT * FROM user_conversations WHERE username = ?
            """, (username,))

            conversations = conn.fetchall()  # TODO: verify how this works because i think this might be returning a weird data structure
            return flask.jsonify({"success": True, "data": conversations}), 201
    else:
        return flask.jsonify({"success": False, "message": "Unauthorized"}), 400
        

@app.route("/chat/<chat_id>", methods=["GET"])
def see_chat_with_chat_id(chat_id):
    """See chat specified by chat_id."""

    username = flask.sessoion.get("username")
    if username:
        with get_db() as conn:
            conn.execute("""
            SELECT * FROM user_conversations WHERE username = ? AND id = ?
            """, (username, chat_id))

            conversation = conn.fetchone()
            return flask.jsonify({"success": True, "data": conversation})
    else:
        return flask.jsonify({"success": False, "message": "Unauthorized"}), 400
            