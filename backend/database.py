import sqlite3
from contextlib import contextmanager


DATABASE = 'app.db'

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Enable dictionary-style access
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            password_salt TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        conn.commit()

        # using user_id here instead of username is a design decision
        # as it's probably faster for sql to gather the data if looking for 
        # a numeric user_id rather than a whole ass username
        conn.execute("""
        CREATE TABLE IF NOT EXISTS user_conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            conversation_data TEXT NOT NULL,
            conversation_title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """)
        # here, conversation_data is a string representing a list of json objects representing messages in the conversation
        # example: 
        # [
        #     {"role": "user", "content": "What's AAPL stock price?", "timestamp": "2023-05-01T12:34:56"},
        #     {"role": "assistant", "content": "AAPL is at $173.50", "timestamp": "2023-05-01T12:35:02"}
        # ]


        # now, when the user enters the chat page, it should default to entering into a new chat
        # however, this new chat shouldn't be added to the database until they actually enter a prompt

        # when a prompt is submitted in a new conversation, we will also prompt the chatbot to come up
        # with a title for this conversation, and store this title in the database


        # when the user goes to the InfoBank page, they can select a conversation

