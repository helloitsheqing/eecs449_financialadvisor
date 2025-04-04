from app import app
from database import get_db
import flask
import pdbp

@app.route("/clear-chats", methods=["DELETE"])
def clear_chats():

    # TODO: ensure session is persisting. once it is, this should be included
    # if flask.session.get("username") != username:
    #     return flask.jsonify({"error": "Unauthorized"}), 403

    # breakpoint()
    username = flask.session.get("username")
    if username:
        with get_db() as conn:
            conn.execute("""
            DELETE * FROM user_conversations WHERE username = ?
            """, (username,))
            return flask.jsonify({"success": True}), 201