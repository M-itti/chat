import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('messages.db')
cursor = conn.cursor()

# Create a table to store messages
cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT NOT NULL,
        message TEXT NOT NULL
    )
''')

# Function to insert a new message into the database
def insert_message(sender, message):
    cursor.execute('''
        INSERT INTO messages (sender, message) VALUES (?, ?)
    ''', (sender, message))
    conn.commit()

# Function to retrieve all messages from the database
def get_all_messages():
    cursor.execute('SELECT * FROM messages')
    return cursor.fetchall()

# Example usage:

# Insert a message
insert_message('Alice', 'Hello, Bob!')
insert_message('Bob', 'Hi, Alice!')

# Retrieve all messages
all_messages = get_all_messages()
for message in all_messages:
    print(f"{message[1]} says: {message[2]}")

# Close the connection when done
conn.close()

