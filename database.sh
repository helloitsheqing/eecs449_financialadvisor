#!/bin/bash

# Database file
DB_FILE="backend/app.db"

# Function to reset the database
reset_db() {
    echo "Resetting database..."
    rm -f "$DB_FILE"
    sqlite3 "$DB_FILE" <<EOF
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    password_salt TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
EOF
    echo "Database reset complete. New empty database created."
}

# Function to populate with test data
populate_db() {
    echo "Populating database with test users..."
    
    # Generate hashes and salts for test users
    # In a real scenario, you'd use your actual hashing logic
    sqlite3 "$DB_FILE" <<EOF
INSERT INTO users (username, password_hash, password_salt) VALUES
    ('admin', '8339760f3b7869eb7f353d275cbe7f60605f4431dafe564fea178c7769de8398', '484e3a5d3cbc161a9554490cc2658e07');
EOF
    echo "Added 3 test users:"
    sqlite3 "$DB_FILE" "SELECT id, username FROM users;"
}

# Main script logic
case "$1" in
    reset)
        reset_db
        ;;
    populate)
        populate_db
        ;;
    *)
        echo "Usage: $0 {reset|populate}"
        echo "  reset    - Completely wipes and recreates the database"
        echo "  populate - Adds test user data to existing database"
        exit 1
esac