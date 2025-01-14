from database import connect_db, connect_db_tech

def create_tables_tech():
    # for the tech assistant database
    conn_tech = connect_db_tech()
    cur_tech = conn_tech.cursor()

    # Create tech_users table
    cur_tech.execute("""
        CREATE TABLE IF NOT EXISTS tech_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT
        )
    """)

    # Create issues table, referencing tech_users instead of users
    cur_tech.execute("""
        CREATE TABLE IF NOT EXISTS issues(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            issue_description TEXT,
            status TEXT,
            FOREIGN KEY(user_id) REFERENCES tech_users(id)  -- Changed reference here
        )
    """)

    conn_tech.commit()
    conn_tech.close()

def insert_mock_data_tech():
    conn_tech = connect_db_tech()
    cur_tech = conn_tech.cursor()

    cur_tech.executemany("""
            INSERT INTO issues(user_id, issue_description, status)
            VALUES(?, ?, ?)
            """,
            [
                (3082278, 'Problems with audio input', 'solved'),
                (3082279, 'Problems with windows activation', 'solved'),
                (3082280, 'Problems with driver installation', 'solved')
            ])

    conn_tech.commit()
    conn_tech.close()

# Function to insert new users into the tech database
def insert_tech_user(name, phone, email):
    conn_tech = connect_db_tech()
    cur_tech = conn_tech.cursor()

    cur_tech.execute("""
        SELECT id FROM tech_users
        WHERE name = ? AND email = ?
    """, (name, email))
    
    existing = cur_tech.fetchone()

    if existing:
        user_id = existing['id']
    else:
        # Insert new user
        cur_tech.execute("""
            INSERT INTO tech_users (name, phone, email) 
            VALUES (?, ?, ?)
        """, (name, phone, email))
        user_id = cur_tech.lastrowid

    conn_tech.commit()
    conn_tech.close()
    
    return user_id

#-------------Clothing store assistant tables-------------------------#

def create_tables():
    conn = connect_db()
    cur = conn.cursor()

    # Create users table for clothing
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT       
        )
    """)

    # Create orders table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product TEXT,
            size TEXT,
            order_date TEXT,
            status TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Create inventory table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS inventory(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT,
            size TEXT,
            quantity INTEGER
        )
    """)

    # Create shipping table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS shipping(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tracking_number TEXT UNIQUE,
            status TEXT,
            estimated_delivery_date TEXT   
        )
    """)
    
    conn.commit()
    conn.close()

def insert_mock_data():
    """Mock data for testing purposes"""
    conn = connect_db()
    cur = conn.cursor()

    # Insert into Inventory
    cur.executemany("""
        INSERT INTO inventory (product, size, quantity)
        VALUES (?, ?, ?)
    """, [
        ('jeans', '32', 10),
        ('jeans', '34', 5),
        ('shirt', 'M', 20)
    ])

    # Insert into Shipping
    cur.executemany("""
        INSERT INTO shipping (tracking_number, status, estimated_delivery_date)
        VALUES (?, ?, ?)
    """, [
        ('123456789', 'In Transit', '2025-01-10'),
        ('987654321', 'Delivered', '2025-01-05')
    ])

    conn.commit()
    conn.close()
