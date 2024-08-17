from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import pandas as pd

app = Flask(__name__)

# Function to fetch data from SQLite and return as DataFrame
def fetch_data(table_name):
    print(f"Fetching data for table: {table_name}")
    conn = sqlite3.connect('C:\\Users\\SMS\\Desktop\\read\\database.sqlite')  # Update path to your SQLite file
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    print("Data processing complete.")
    return df

# Route to display data from SQLite in HTML
@app.route('/')
def display_data():
    table_names = ['ورقة1']  # List of your sheet names
    data = {}
    for table_name in table_names:
        print(f"Processing table: {table_name}")
        data[table_name] = fetch_data(table_name)
    
    print("Rendering template with data.")
    return render_template('index.html', data=data)

# Route to display data for printing
@app.route('/printt')
def printt():
    table_names = ['ورقة1']  # Update this with your actual table names
    data = {}
    
    for table_name in table_names:
        data[table_name] = fetch_data(table_name)
    
    return render_template('print.html', data=data)

# Route to add a new user
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        laqap = request.form['laqap']
        nofAosra = request.form['nofAosra']
        inoan=request.form['inoan']
        phone=request.form['phone']

        # Add the user to the database
        try:
            conn = sqlite3.connect('C:\\Users\\SMS\\Desktop\\read\\database.sqlite')  # Update path to your SQLite file
            cursor = conn.cursor()
            cursor.execute("INSERT INTO ورقة1 (name, email, userID) VALUES (?, ?, ?)", (name, email, userID))
            conn.commit()
            conn.close()
            print(f"User {name} added successfully.")
            return redirect(url_for('display_data'))
        except Exception as e:
            print(f"Error adding user: {e}")
            return f"An error occurred: {e}"

    return render_template('add_user.html')

if __name__ == '__main__':
    app.run(debug=True)
