from app import app
from database import get_db
import flask


@app.route("/new_chat")
def create_new_chat():
    """Create a new chat and insert to db."""
    username = flask.session.get("username")
    if username: 
        # wait for user to submit a prompt
        # then, wait for bot to return response
        # prompt the bot for a title
        # insert into database
        # redirect to chat/<this chat_id>
        return