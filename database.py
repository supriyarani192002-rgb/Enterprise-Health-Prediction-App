import sqlite3

def get_connection():
    # check_same_thread=False is needed for Streamlit
    return sqlite3.connect('patients.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            dob TEXT,
            email TEXT,
            glucose REAL,
            haemoglobin REAL,
            cholesterol REAL,
            remarks TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_patient(name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO patients (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, dob, email, glucose, haemoglobin, cholesterol, remarks))
    conn.commit()
    conn.close()

def get_all_patients():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM patients')
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_patient(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM patients WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def update_patient(id, name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE patients 
        SET full_name=?, dob=?, email=?, glucose=?, haemoglobin=?, cholesterol=?, remarks=?
        WHERE id=?
    ''', (name, dob, email, glucose, haemoglobin, cholesterol, remarks, id))
    conn.commit()
    conn.close()