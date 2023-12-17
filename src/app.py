from flask import Flask, render_template, request
import os
import sqlite3

app = Flask(__name__)

# Function to create a connection to the SQLite database
def create_connection():
    folder_path='/home/chaca/Documents/Tese/Tese/src/'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    db_file_path = os.path.join(folder_path, 'database.db')
    return sqlite3.connect(db_file_path)

# Function to execute a query and fetch results
def execute_query(query, params=()):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for handling the search query
@app.route('/search', methods=['POST'])
def search():
    # Get the user's query from the form
    user_query = request.form['query']

    # Execute a simple search query on the database
    query = "SELECT * FROM tabela WHERE name='" + user_query + "'"
    result = execute_query(query)

    # Render the results on the search results page
    return render_template('search_results.html', result=result)

if __name__ == '__main__':
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tabela (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER
    )
''')

    # Example 2: Insert multiple records
    data_to_insert = [
        (1, 'Alice Smith', 30),
        (2, 'Bob Johnson', 22),
        (3, 'Eva Williams', 28)
    ]
    cursor.executemany("INSERT OR IGNORE INTO tabela (id, name, age) VALUES (?, ?, ?)", data_to_insert)

    conn.commit()
    conn.close()
    app.run(debug=True)