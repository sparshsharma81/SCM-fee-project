from flask import Flask, render_template, redirect, url_for, request, g
import sqlite3

app = Flask(__name__)

# SQLite database setup
DATABASE = 'resume_database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

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
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            INSERT INTO resumes (name, email, phone, address, objective, education, experience)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, email, phone, address, objective, education, experience))
        conn.commit()
        conn.close()

        # Redirect to the thank-you page after successfully creating the resume
        return render_template('resume_created.html', user_name=name, user_email=email, user_phone=phone,
                               user_address=address, user_objective=objective, user_education=education,
                               user_experience=experience)

    return render_template('index.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/show_database')
def show_database():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM resumes')
    resumes = c.fetchall()
    conn.close()
    return render_template('show_database.html', resumes=resumes)

if __name__ == '__main__':
    app.run(debug=True)
