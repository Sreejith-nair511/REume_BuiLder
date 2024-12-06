import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Create the uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    education = request.form['education']
    experience = request.form['experience']
    skills = request.form['skills']
    template = request.form['template'] or 'default'
    
    image = request.files['image']
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    else:
        image_url = None
    
    conn = get_db_connection()
    conn.execute('INSERT INTO resumes (name, email, phone, education, experience, skills, image_url, template) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                 (name, email, phone, education, experience, skills, image_url, template))
    conn.commit()
    conn.close()
    
    return redirect(url_for('resume', name=name))

@app.route('/resume/<name>')
def resume(name):
    conn = get_db_connection()
    resume = conn.execute('SELECT * FROM resumes WHERE name = ?', (name,)).fetchone()
    conn.close()
    template = resume['template'] or 'default'
    return render_template(f'resume_{template}.html', resume=resume)

if __name__ == '__main__':
    app.run(debug=True)
