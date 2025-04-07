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


@app.route("/chats", methods=["DELETE"])
def see_chats():
    """See all chats in db."""

    username = flask.session.get("username")
    if username:
        with get_db() as conn:
            # extract user_id from db
            conn.execute("""
            SELECT id FROM users WHERE username = ?
            """, (username,))
            user_id = conn.fetchone()  # this might be wrong, i forgot what fetchone() does but if anything should be a quick fix

            conn.execute("""
            SELECT * FROM user_conversations WHERE user_id = ?
            """, (user_id,))

            conversations = conn.fetchall()
            return flask.jsonify({"success": True, "data": conversations}), 201
        

@app.route("/chat/<chat_id>", methods=["GET"])
def see_chat_with_chat_id(chat_id):
    """See chat specified by chat_id."""
    
    username = flask.sessoion.get("username")
    if username:
        with get_db() as conn:
            conn.execute("""
            SELECT id FROM users WHERE username = ?
            """, (username,))
            user_id = conn.fetchone()  # this might be wrong, i forgot what fetchone() does but if anything should be a quick fix

            conn.execute("""
            SELECT * FROM user_conversations WHERE user_id = ? AND id = ?
            """, (user_id, chat_id))

            conversation = conn.fetchone()
            return flask.jsonify({"success": True, "data": conversation})
            