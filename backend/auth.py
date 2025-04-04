"""
This file contains everything authentication so far. 
Process goes as such: 
    When registering a new user: 
        1) generate a random salt
        2) hash the password + salt
        3) store (username, password_hash, password_salt) tuple in db

    When verifying a user:
        1) extract the (username, password_hash, password_salt) tuple from db
        2) calculate hash of inputted password with salt stored in db
        3) if is equal to password_hash stored in db, user is legit


***
Return objects in registration and verification functions could be changed,
but will be up to implementation decisions. This is good for now I think. 
***
"""

# auth.py
from database import get_db
import sqlite3
import binascii
import os
import hashlib
# from app import app
from flask import request, render_template, make_response, Blueprint, jsonify, session, redirect
import pdbp

SALT_LENGTH = 16  # 16 bytes = 32 hex characters


auth_bp = Blueprint('auth', __name__)


def generate_salt():
    """Generate a random salt for password storing."""
    return binascii.hexlify(os.urandom(SALT_LENGTH)).decode('utf-8')


def hash_password(password, salt):
    """Create SHA-256 hash with salt"""
    salted_password = password.encode('utf-8') + salt.encode('utf-8')
    return hashlib.sha256(salted_password).hexdigest()


def register_user(username, password):
    """Add user information to the database."""
    # generate random x-digit length salt from the password
    # hash the password
    # store username, password_hash, password_salt

    salt = generate_salt()
    password_hash = hash_password(password, salt)
    with get_db() as conn:
        try:
            conn.execute(
                "INSERT INTO users (username, password_hash, password_salt) VALUES (?, ?, ?)",
                (username, password_hash, salt)
            )
            conn.commit()
            # return conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            # if "username" not in session:
            session["username"] = username 
            session.permanent = True
            session.modified = True

            response = jsonify({
                "success": True,
                "message": "Signup successful",
                "username": username
            })

            response.set_cookie(
                'laughing_stocks_session',
                value=session["session_id"],
                httponly=True,
                samesite='Lax'
            )
            return response
        
        except sqlite3.IntegrityError:
            return {"success": False, 
                    "message": "Username already taken."}


def verify_user(username, password):
    """Extract (username, password_hash, password_salt) tuple from db."""
    with get_db() as conn:
        user_data = conn.execute(
            "SELECT password_hash, password_salt FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        actual_password_hash = user_data["password_hash"]
        actual_password_salt = user_data["password_salt"]

        input_password_hash = hash_password(password, actual_password_salt)

        if input_password_hash == actual_password_hash:
            # we know this user is legit and entered the correct password
            # breakpoint()
            # if "username" not in session:
            session["username"] = username 
            session.permanent = True
            session.modified = True


            response = jsonify({
                "success": True,
                "message": "Login successful",
                "username": username
            })

            response.set_cookie(
                'laughing_stocks_session',
                value=session["session_id"],
                httponly=True,
                samesite='Lax'
            )
            return response
        else:
            return {"success": False,
                    "message": "User authentication failed."}, 401  # is this the right code?

    return None


# Clear session on logout
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# these functions are currently under testing mode, which is why there is an html string object
@auth_bp.route("/auth/login", methods=["POST", "OPTIONS"])
def login():
    print("session: ", session)
    if request.method == 'OPTIONS':
        return _build_preflight_response()

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    return verify_user(username, password)


@auth_bp.route("/auth/signup", methods=["POST", "OPTIONS"])
def signup():
    # breakpoint()

    if request.method == 'OPTIONS':
        return _build_preflight_response()

    # breakpoint()
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    return register_user(username, password)


def _build_preflight_response():
    response = jsonify()
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    response.headers.add("Access-Control-Allow-Credentials", "true")  # Crucial for sessions
    response.headers.add("Content-Type", "application/json")
    return response
