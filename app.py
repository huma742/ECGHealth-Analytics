from flask import Flask, jsonify, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ecg_health'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/patients')
def get_patients():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cleanned")
    rows = cur.fetchall()
    cur.close()
    patients = []
    for i, row in enumerate(rows):
        patients.append({
            'id': i+1,
            'age': row[0],
            'sex': row[1],
            'cp': row[2],
            'trestbps': row[3],
            'chol': row[4],
            'fbs': row[5],
            'restecg': row[6],
            'thalch': row[7],
            'exang': row[8],
            'oldpeak': row[9],
            'num': row[10]
        })
    return jsonify(patients)

if __name__ == '__main__':
    app.run(debug=True)