from app import app
from database import get_db
import flask

@app.route("/clear_chats/<username>", methods=["DELETE"])
def clear_chats(username):
    if flask.session.get("username") != username:
        return flask.jsonify({"error": "Unauthorized"}), 403

    with get_db() as conn:
        conn.execute("""
        DELETE * FROM user_conversations WHERE username = ?
        """, (username,))
        return flask.jsonify({"success": True}), 201