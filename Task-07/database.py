import sqlite3


DB_NAME = "pirate.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            berries INTEGER DEFAULT 100
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            user_id TEXT,
            item_name TEXT,
            active INTEGER DEFAULT 0,
            PRIMARY KEY (user_id, item_name),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            action TEXT,
            amount INTEGER,
            target_id TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def create_user(user_id, username):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO users
        (user_id, username, berries)
        VALUES (?, ?, 100)
    """, (str(user_id), username))

    conn.commit()
    conn.close()


def get_bounty(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT berries FROM users WHERE user_id = ?",
        (str(user_id),)
    )

    result = cursor.fetchone()

    conn.close()

    if result is None:
        return 0

    return result[0]


def update_bounty(user_id, amount):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET berries = berries + ?
        WHERE user_id = ?
    """, (amount, str(user_id)))

    conn.commit()
    conn.close()


def add_inventory_item(user_id, item_name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO inventory
        (user_id, item_name, active)
        VALUES (?, ?, 0)
    """, (str(user_id), item_name))

    conn.commit()
    conn.close()


def get_inventory(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT item_name
        FROM inventory
        WHERE user_id = ?
    """, (str(user_id),))

    items = [row[0] for row in cursor.fetchall()]

    conn.close()

    return items


def log_transaction(
    user_id,
    action,
    amount=0,
    target_id=None
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions
        (user_id, action, amount, target_id)
        VALUES (?, ?, ?, ?)
    """, (
        str(user_id),
        action,
        amount,
        str(target_id) if target_id else None
    ))

    conn.commit()
    conn.close()


def get_top_users(limit=5):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username, berries
        FROM users
        ORDER BY berries DESC
        LIMIT ?
    """, (limit,))

    users = cursor.fetchall()

    conn.close()

    return users
