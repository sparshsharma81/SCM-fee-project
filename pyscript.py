from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Database initialization (run only once)
def init_db():
    conn = sqlite3.connect('resumes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            objective TEXT,
            education TEXT,
            experience TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()  # Initialize the database

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_resume', methods=['POST'])
def create_resume():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        objective = request.form.get('objective')
        education = request.form.get('education')
        experience = request.form.get('experience')

        # Save data to the database
        conn = sqlite3.connect('resumes.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO resumes (name, email, phone, address, objective, education, experience)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, email, phone, address, objective, education, experience))
        conn.commit()
        conn.close()

        # Redirect to a thank-you page or any other page
        return render_template('thank_you.html', user_name=name, user_email=email, user_phone=phone,
                               user_address=address, user_objective=objective, user_education=education,
                               user_experience=experience)

if __name__ == '__main__':
    app.run(debug=True)
