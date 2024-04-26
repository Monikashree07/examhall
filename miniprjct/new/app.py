
# from flask import Flask, render_template, request, redirect, url_for
# import sqlite3

# app = Flask(__name__)

# # Function to connect to the database
# def get_db():
#     conn = sqlite3.connect('seating.db')
#     conn.row_factory = sqlite3.Row
#     return conn

# # Function to create the seating arrangement table
# def create_table():
#     conn = get_db()
#     cursor = conn.cursor()
#     cursor.execute('''DROP TABLE IF EXISTS seating_arrangement''')
#     cursor.execute('''CREATE TABLE IF NOT EXISTS seating_arrangement (
#                     id INTEGER PRIMARY KEY,
#                     class_name TEXT NOT NULL,
#                     room_name TEXT NOT NULL,
#                     row_num INTEGER NOT NULL,
#                     col_num INTEGER NOT NULL,
#                     roll_number INTEGER,
#                     year INTEGER NOT NULL
#                     )''')
#     conn.commit()
#     conn.close()

# # Create the seating arrangement table
# create_table()

# # Define user credentials
# user_credentials = {
#     'admin': 'admin',
#     'student': 'student'
# }

# # Homepage
# @app.route('/')
# def home():
#     return render_template('index.html')

# # Student login page
# @app.route('/student', methods=['GET', 'POST'])
# def student():
#     if request.method == 'POST':
#         return redirect(url_for('select_class_and_year'))  # Redirect to class and year selection page
#     return render_template('student.html')

# # Login page
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         userid = request.form['userid']
#         password = request.form['password']
       
#         if userid in user_credentials and user_credentials[userid] == password:
#             if userid == 'admin':
#                 return redirect(url_for('dashboard'))
#             elif userid == 'student':
#                 return redirect(url_for('select_class_and_year'))
#         else:
#             return render_template('login.html', message='Invalid credentials. Please try again.')
    
#     return render_template('login.html')

# # Dashboard page
# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html')

# # Seating arrangement page
# @app.route('/seating', methods=['GET', 'POST'])
# def seating():
#     if request.method == 'POST':
#         class_name = request.form['class_name']
#         year = request.form['year']
#         room_from = request.form['room_from']  # Changed from int to str
#         room_to = request.form['room_to']  # Changed from int to str
#         roll_from = int(request.form['roll_from'])
#         roll_to = int(request.form['roll_to'])
#         rows_per_room = int(request.form['rows_per_room'])
#         cols_per_room = int(request.form['cols_per_room'])
        
#         generate_seating_arrangement(class_name, year, room_from, room_to, roll_from, roll_to, rows_per_room, cols_per_room)
        
#         return redirect(url_for('result', class_name=class_name, year=year))
    
#     return render_template('seating.html')

# # Class and year selection page for students
# @app.route('/select_class_and_year', methods=['GET', 'POST'])
# def select_class_and_year():
#     if request.method == 'POST':
#         class_name = request.form['class_name']
#         year = request.form['year']
#         roll_number = request.form['roll_number']

#         return redirect(url_for('student_result', class_name=class_name, year=year, roll_number=roll_number))

#     return render_template('select_class_and_year.html')

# # Result page for seating arrangement
# @app.route('/result/<class_name>/<year>')
# def result(class_name, year):
#     db = get_db()
#     cursor = db.cursor()
#     cursor.execute("SELECT room_name, row_num, col_num, roll_number FROM seating_arrangement WHERE class_name=? AND year=? ORDER BY room_name, row_num, col_num", (class_name, year))
#     seating_arrangement = cursor.fetchall()
#     cursor.close()

#     if not seating_arrangement:
#         return "No seating arrangement available"

#     arranged_seating = {}
#     for room_name, row_num, col_num, roll_number in seating_arrangement:
#         if room_name not in arranged_seating:
#             arranged_seating[room_name] = {'seats': []}
#         arranged_seating[room_name]['seats'].append((row_num, col_num, roll_number))

#     return render_template('result.html', class_name=class_name, year=year, seating_arrangement=arranged_seating)

# # Result page for individual student
# @app.route('/result/student/<class_name>/<year>/<int:roll_number>')
# def student_result(class_name, year, roll_number):
#     db = get_db()
#     cursor = db.cursor()
#     cursor.execute("SELECT room_name, row_num, col_num, roll_number FROM seating_arrangement WHERE class_name=? AND year=? AND roll_number=? ORDER BY room_name, row_num, col_num", (class_name, year, roll_number))
#     seating_arrangement = cursor.fetchall()
#     cursor.close()

#     arranged_seating = {}
#     for room_name, row_num, col_num, roll_number in seating_arrangement:
#         if room_name not in arranged_seating:
#             arranged_seating[room_name] = {'seats': []}
#         arranged_seating[room_name]['seats'].append((row_num, col_num, roll_number))

#     return render_template('student_result.html', class_name=class_name, year=year, roll_number=roll_number, seating_arrangement=arranged_seating)

# import random  # Import the random module

# def generate_seating_arrangement(class_name, year, room_from, room_to, roll_from, roll_to, rows_per_room, cols_per_room):
#     db = get_db()
#     cursor = db.cursor()
    
#     # Extract the numeric part of the room numbers
#     room_from_numeric = int(room_from[1:])  # Extract the numeric part after the first character
#     room_to_numeric = int(room_to[1:])  # Extract the numeric part after the first character
    
#     for room_num in range(room_from_numeric, room_to_numeric + 1):
#         room_name = f'{room_from[0]}{room_num}'  # Combine the first character with the numeric part
        
#         # Get existing seating arrangement for the room
#         cursor.execute("SELECT row_num, col_num FROM seating_arrangement WHERE room_name=? AND year=?", (room_name, year))
#         existing_seats = cursor.fetchall()
        
#         # Create a set of occupied seats for fast lookup
#         occupied_seats = set((row_num, col_num) for row_num, col_num in existing_seats)
        
#         # Determine the starting column for this room
#         start_col_num = 1
#         if existing_seats:
#             # If seats are already allocated, start from column 2
#             start_col_num = 2
        
#         # Shuffle the order of rows and columns to introduce randomness
#         rows_order = list(range(1, rows_per_room + 1))
#         random.shuffle(rows_order)
#         cols_order = list(range(start_col_num, cols_per_room + 1, 2))
#         random.shuffle(cols_order)
        
#         # Allocate seats alternatively starting from shuffled rows and columns
#         for row_num in rows_order:
#             for col_num in cols_order:
#                 if (row_num, col_num) not in occupied_seats:
#                     # Allocate the seat with the current roll number if it's within the specified range
#                     if roll_from <= roll_to:
#                         cursor.execute("INSERT INTO seating_arrangement (class_name, room_name, row_num, col_num, roll_number, year) VALUES (?, ?, ?, ?, ?, ?)",
#                                        (class_name, room_name, row_num, col_num, roll_from, year))
#                         roll_from += 1
#                     else:
#                         # Break out of the loop if roll_from exceeds roll_to
#                         break
        
#     db.commit()
#     db.close()


# if __name__ == '__main__':
#     app.run(debug=True)







# from flask import Flask, render_template, request, redirect, url_for
# import sqlite3

# app = Flask(__name__)

# # Function to connect to the database
# def get_db():
#     conn = sqlite3.connect('seating.db')
#     conn.row_factory = sqlite3.Row
#     return conn

# # Function to create the seating arrangement table
# def create_table():
#     conn = get_db()
#     cursor = conn.cursor()
#     cursor.execute('''DROP TABLE IF EXISTS seating_arrangement''')
#     cursor.execute('''CREATE TABLE IF NOT EXISTS seating_arrangement (
#                     id INTEGER PRIMARY KEY,
#                     class_name TEXT NOT NULL,
#                     room_name TEXT NOT NULL,
#                     row_num INTEGER NOT NULL,
#                     col_num INTEGER NOT NULL,
#                     roll_number INTEGER,
#                     year INTEGER NOT NULL
#                     )''')
#     conn.commit()
#     conn.close()

# # Create the seating arrangement table
# create_table()

# # Define user credentials
# user_credentials = {
#     'admin': 'admin',
#     'student': 'student'
# }

# # Homepage
# @app.route('/')
# def home():
#     return render_template('index.html')

# # Student login page
# @app.route('/student', methods=['GET', 'POST'])
# def student():
#     if request.method == 'POST':
#         return redirect(url_for('select_class_and_year'))  # Redirect to class and year selection page
#     return render_template('student.html')

# # Login page
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         userid = request.form['userid']
#         password = request.form['password']
       
#         if userid in user_credentials and user_credentials[userid] == password:
#             if userid == 'admin':
#                 return redirect(url_for('dashboard'))
#             elif userid == 'student':
#                 return redirect(url_for('select_class_and_year'))
#         else:
#             return render_template('login.html', message='Invalid credentials. Please try again.')
    
#     return render_template('login.html')

# # Dashboard page
# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html')

# # Seating arrangement page
# @app.route('/seating', methods=['GET', 'POST'])
# def seating():
#     if request.method == 'POST':
#         class_name = request.form['class_name']
#         year = request.form['year']
#         room_from = request.form['room_from']  # Changed from int to str
#         room_to = request.form['room_to']  # Changed from int to str
#         roll_from = int(request.form['roll_from'])
#         roll_to = int(request.form['roll_to'])
#         rows_per_room = int(request.form['rows_per_room'])
#         cols_per_room = int(request.form['cols_per_room'])
        
#         generate_seating_arrangement(class_name, year, room_from, room_to, roll_from, roll_to, rows_per_room, cols_per_room)
        
#         return redirect(url_for('result', class_name=class_name, year=year))
    
#     return render_template('seating.html')

# # Class and year selection page for students
# @app.route('/select_class_and_year', methods=['GET', 'POST'])
# def select_class_and_year():
#     if request.method == 'POST':
#         class_name = request.form['class_name']
#         year = request.form['year']
#         roll_number = request.form['roll_number']

#         return redirect(url_for('student_result', class_name=class_name, year=year, roll_number=roll_number))

#     return render_template('select_class_and_year.html')

# # Result page for seating arrangement
# @app.route('/result/<class_name>/<year>')
# def result(class_name, year):
#     db = get_db()
#     cursor = db.cursor()
#     cursor.execute("SELECT room_name, row_num, col_num, roll_number FROM seating_arrangement WHERE class_name=? AND year=? ORDER BY room_name, row_num, col_num", (class_name, year))
#     seating_arrangement = cursor.fetchall()
#     cursor.close()

#     if not seating_arrangement:
#         return "No seating arrangement available"

#     arranged_seating = {}
#     for room_name, row_num, col_num, roll_number in seating_arrangement:
#         if room_name not in arranged_seating:
#             arranged_seating[room_name] = {'seats': []}
#         arranged_seating[room_name]['seats'].append((row_num, col_num, roll_number))

#     return render_template('result.html', class_name=class_name, year=year, seating_arrangement=arranged_seating)

# # Result page for individual student
# @app.route('/result/student/<class_name>/<year>/<int:roll_number>')
# def student_result(class_name, year, roll_number):
#     db = get_db()
#     cursor = db.cursor()
#     cursor.execute("SELECT room_name, row_num, col_num, roll_number FROM seating_arrangement WHERE class_name=? AND year=? AND roll_number=? ORDER BY room_name, row_num, col_num", (class_name, year, roll_number))
#     seating_arrangement = cursor.fetchall()
#     cursor.close()

#     arranged_seating = {}
#     for room_name, row_num, col_num, roll_number in seating_arrangement:
#         if room_name not in arranged_seating:
#             arranged_seating[room_name] = {'seats': []}
#         arranged_seating[room_name]['seats'].append((row_num, col_num, roll_number))

#     return render_template('student_result.html', class_name=class_name, year=year, roll_number=roll_number, seating_arrangement=arranged_seating)

# def generate_seating_arrangement(class_name, year, room_from, room_to, roll_from, roll_to, rows_per_room, cols_per_room):
#     db = get_db()
#     cursor = db.cursor()
    
#     # Extract the numeric part of the room numbers
#     room_from_numeric = int(room_from[1:])  # Extract the numeric part after the first character
#     room_to_numeric = int(room_to[1:])  # Extract the numeric part after the first character
    
#     for room_num in range(room_from_numeric, room_to_numeric + 1):
#         room_name = f'{room_from[0]}{room_num}'  # Combine the first character with the numeric part
        
#         # Get existing seating arrangement for the room
#         cursor.execute("SELECT row_num, col_num FROM seating_arrangement WHERE room_name=? AND year=?", (room_name, year))
#         existing_seats = cursor.fetchall()
        
#         # Create a set of occupied seats for fast lookup
#         occupied_seats = set((row_num, col_num) for row_num, col_num in existing_seats)
        
#         # Determine the starting column for this room
#         start_col_num = 1
#         if existing_seats:
#             # If seats are already allocated, start from column 2
#             start_col_num = 2
        
#         # Allocate seats alternatively starting from start_col_num
#         for row_num in range(1, rows_per_room + 1):
#             for col_num in range(start_col_num, cols_per_room  + 1, 2):  # Increment by 2 to leave one space between seats
#                 if (row_num, col_num) not in occupied_seats:
#                     # Allocate the seat with the current roll number if it's within the specified range
#                     if roll_from <= roll_to:
#                         cursor.execute("INSERT INTO seating_arrangement (class_name, room_name, row_num, col_num, roll_number, year) VALUES (?, ?, ?, ?, ?, ?)",
#                                        (class_name, room_name, row_num, col_num, roll_from, year))
#                         roll_from += 1
#                     else:
#                         # Break out of the loop if roll_from exceeds roll_to
#                         break
        
#     db.commit()
#     db.close()


# if __name__ == '__main__':
#     app.run(debug=True)






from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import random

app = Flask(__name__)

# Function to connect to the database
def get_db():
    conn = sqlite3.connect('seating.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to create the seating arrangement table
def create_table():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE IF EXISTS seating_arrangement''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS seating_arrangement (
                    id INTEGER PRIMARY KEY,
                    class_name TEXT NOT NULL,
                    room_name TEXT NOT NULL,
                    row_num INTEGER NOT NULL,
                    col_num INTEGER NOT NULL,
                    roll_number INTEGER,
                    year INTEGER NOT NULL
                    )''')
    conn.commit()
    conn.close()

# Create the seating arrangement table
create_table()

# Define user credentials
user_credentials = {
    'admin': 'admin',
    'student': 'student'
}

# Homepage
@app.route('/')
def home():
    return render_template('index.html')

# Student login page
@app.route('/student', methods=['GET', 'POST'])
def student():
    if request.method == 'POST':
        return redirect(url_for('select_class_and_year'))  # Redirect to class and year selection page
    return render_template('student.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
       
        if userid in user_credentials and user_credentials[userid] == password:
            if userid == 'admin':
                return redirect(url_for('dashboard'))
            elif userid == 'student':
                return redirect(url_for('select_class_and_year'))
        else:
            return render_template('login.html', message='Invalid credentials. Please try again.')
    
    return render_template('login.html')

# Dashboard page
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Seating arrangement page
@app.route('/seating', methods=['GET', 'POST'])
def seating():
    if request.method == 'POST':
        class_name = request.form['class_name']
        year = request.form['year']
        room_from = request.form['room_from']  # Changed from int to str
        room_to = request.form['room_to']  # Changed from int to str
        roll_from = int(request.form['roll_from'])
        roll_to = int(request.form['roll_to'])
        rows_per_room = int(request.form['rows_per_room'])
        cols_per_room = int(request.form['cols_per_room'])
        
        generate_seating_arrangement(class_name, year, {'room_from': room_from, 'room_to': room_to, 'roll_from': roll_from, 'roll_to': roll_to}, rows_per_room, cols_per_room)
        
        return redirect(url_for('result', class_name=class_name, year=year))
    
    return render_template('seating.html')


# Class and year selection page for students
@app.route('/select_class_and_year', methods=['GET', 'POST'])
def select_class_and_year():
    if request.method == 'POST':
        class_name = request.form['class_name']
        year = request.form['year']
        roll_number = request.form['roll_number']

        return redirect(url_for('student_result', class_name=class_name, year=year, roll_number=roll_number))

    return render_template('select_class_and_year.html')

# Result page for seating arrangement
@app.route('/result/<class_name>/<year>')
def result(class_name, year):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT room_name, row_num, col_num, roll_number FROM seating_arrangement WHERE class_name=? AND year=? ORDER BY room_name, row_num, col_num", (class_name, year))
    seating_arrangement = cursor.fetchall()
    cursor.close()

    if not seating_arrangement:
        return "No seating arrangement available"

    arranged_seating = {}
    for room_name, row_num, col_num, roll_number in seating_arrangement:
        if room_name not in arranged_seating:
            arranged_seating[room_name] = {'seats': []}
        arranged_seating[room_name]['seats'].append((row_num, col_num, roll_number))

    return render_template('result.html', class_name=class_name, year=year, seating_arrangement=arranged_seating)

# Result page for individual student
@app.route('/result/student/<class_name>/<year>/<int:roll_number>')
def student_result(class_name, year, roll_number):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT room_name, row_num, col_num, roll_number FROM seating_arrangement WHERE class_name=? AND year=? AND roll_number=? ORDER BY room_name, row_num, col_num", (class_name, year, roll_number))
    seating_arrangement = cursor.fetchall()
    cursor.close()

    arranged_seating = {}
    for room_name, row_num, col_num, roll_number in seating_arrangement:
        if room_name not in arranged_seating:
            arranged_seating[room_name] = {'seats': []}
        arranged_seating[room_name]['seats'].append((row_num, col_num, roll_number))

    return render_template('student_result.html', class_name=class_name, year=year, roll_number=roll_number, seating_arrangement=arranged_seating)



def generate_seating_arrangement(class_name, year, individual, rows_per_room, cols_per_room):
    db = get_db()
    cursor = db.cursor()
    
    # Extract room information from the individual
    room_from = individual['room_from']
    room_to = individual['room_to']
    roll_from = individual['roll_from']
    roll_to = individual['roll_to']
    
    # Extract the numeric part of the room numbers
    room_from_numeric = int(room_from[1:])  # Extract the numeric part after the first character
    room_to_numeric = int(room_to[1:])  # Extract the numeric part after the first character
    
    for room_num in range(room_from_numeric, room_to_numeric + 1):
        room_name = f'{room_from[0]}{room_num}'  # Combine the first character with the numeric part
        
        # Get existing seating arrangement for the room
        cursor.execute("SELECT row_num, col_num FROM seating_arrangement WHERE room_name=? AND year=?", (room_name, year))
        existing_seats = cursor.fetchall()
        
        # Create a set of occupied seats for fast lookup
        occupied_seats = set((row_num, col_num) for row_num, col_num in existing_seats)
        
        # Determine the starting column for this room
        start_col_num = 1
        if existing_seats:
            # If seats are already allocated, start from column 2
            start_col_num = 2
        
        # Shuffle the order of rows and columns to introduce randomness
        rows_order = list(range(1, rows_per_room + 1))
        random.shuffle(rows_order)
        cols_order = list(range(start_col_num, cols_per_room + 1, 2))
        random.shuffle(cols_order)
        
        # Allocate seats alternatively starting from shuffled rows and columns
        for row_num in rows_order:
            for col_num in cols_order:
                if (row_num, col_num) not in occupied_seats:
                    # Allocate the seat with the current roll number if it's within the specified range
                    if roll_from <= roll_to:
                        cursor.execute("INSERT INTO seating_arrangement (class_name, room_name, row_num, col_num, roll_number, year) VALUES (?, ?, ?, ?, ?, ?)",
                                       (class_name, room_name, row_num, col_num, roll_from, year))
                        roll_from += 1
                    else:
                        # Break out of the loop if roll_from exceeds roll_to
                        break
        
    db.commit()
    db.close()


if __name__ == '__main__':
    app.run(debug=True)






