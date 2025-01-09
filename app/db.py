# db.py
import sqlite3
import os
import secrets

from faker import Faker
import uuid

DATABASE = 'users.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def seed():
    fake = Faker('no_NO')

    create_user('admin', os.getenv("ADMIN_PASSWORD", str(uuid.uuid4())))
    set_vote("admin", "borat")

    for _ in range(1000):
        username = fake.user_name() + str(secrets.randbelow(99))
        password = str(uuid.uuid4())
        create_user(username, password)
        set_vote(username, "trump" if secrets.randbelow(2) == 1 else "harris")


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            has_voted BOOLEAN DEFAULT FALSE,
            vote TEXT DEFAULT NULL
        )
    ''')
    if get_user_by_username('admin') is None:
        seed()
    conn.commit()
    conn.close()


def create_user(username, password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
        ''', (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def get_user_by_username(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def verify_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Note: Fix better verification
    query = f"SELECT * FROM users WHERE username = '{username}' AND password_hash = '{password}'"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    if result:
        return True
    return False


def set_vote(username, candidate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users
            SET vote = ?, has_voted = TRUE
            WHERE username = ?
        ''', (candidate, username))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error setting vote: {e}")
        return False


def get_vote(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT vote FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    if result and result['vote']:
        return result['vote']
    else:
        return None


def get_all_users_votes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username, vote FROM users')
    users = cursor.fetchall()
    conn.close()
    return users


def get_all_usernames():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM users')
    users = cursor.fetchall()
    conn.close()
    return [user['username'] for user in users]


def get_vote_counts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT vote, COUNT(*) as count
        FROM users
        WHERE vote IS NOT NULL
        GROUP BY vote
    ''')
    results = cursor.fetchall()
    conn.close()

    vote_counts = {}
    for row in results:
        vote = row['vote'].lower()
        count = row['count']
        vote_counts[vote] = count
    return vote_counts
