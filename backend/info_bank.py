from app import app
from database import get_db
import flask
import pdbp

@app.route("/clear-chats", methods=["DELETE"])
def clear_chats():

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
            