from flask import Flask, jsonify, render_template
import sqlite3
import csv
import os

app = Flask(__name__)

DB_PATH = 'ecg_health.db'

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age TEXT, sex TEXT, cp TEXT, trestbps TEXT,
            chol TEXT, fbs TEXT, restecg TEXT, thalch TEXT,
            exang TEXT, oldpeak TEXT, num TEXT
        )''')
        with open('cleanned.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute('INSERT INTO patients VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?)',
                    (row['age'], row['sex'], row['cp'], row['trestbps'],
                     row['chol'], row['fbs'], row['restecg'], row['thalch'],
                     row['exang'], row['oldpeak'], row['num']))
        conn.commit()
        conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/patients')
def get_patients():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients")
    rows = cur.fetchall()
    conn.close()
    patients = []
    for row in rows:
        patients.append({
            'id': row[0], 'age': row[1], 'sex': row[2],
            'cp': row[3], 'trestbps': row[4], 'chol': row[5],
            'fbs': row[6], 'restecg': row[7], 'thalch': row[8],
            'exang': row[9], 'oldpeak': row[10], 'num': row[11]
        })
    return jsonify(patients)

if __name__ == '__main__':
    app.run(debug=True)