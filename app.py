from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'gizli-anahtar-123'
DB_PATH = 'messages.db'

# Admin şifresi
ADMIN_PASSWORD = 'admin123'

# Email ayarları (kendi Gmail bilgilerini gir)
EMAIL_SENDER = os.getenv('EMAIL_SENDER', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER', '')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def send_email(name, email, message):
    if not EMAIL_SENDER or not EMAIL_PASSWORD or not EMAIL_RECEIVER:
        return
    try:
        body = f"Yeni mesaj!\n\nİsim: {name}\nEmail: {email}\nMesaj: {message}"
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = f'Yeni İletişim Mesajı - {name}'
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Email gönderilemedi: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not name or not email or not message:
            return render_template('contact.html', error="Tüm alanları doldurun.")

        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            'INSERT INTO messages (name, email, message) VALUES (?, ?, ?)',
            (name, email, message)
        )
        conn.commit()
        conn.close()

        send_email(name, email, message)

        return render_template('contact.html', success="Mesajınız alındı, teşekkürler!")
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('messages'))
        return render_template('login.html', error="Şifre yanlış!")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('login'))

@app.route('/messages')
def messages():
    if not session.get('admin'):
        return redirect(url_for('login'))
    search = request.args.get('search', '')
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    if search:
        rows = conn.execute(
            'SELECT * FROM messages WHERE name LIKE ? OR email LIKE ? OR message LIKE ? ORDER BY created_at DESC',
            (f'%{search}%', f'%{search}%', f'%{search}%')
        ).fetchall()
    else:
        rows = conn.execute('SELECT * FROM messages ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('messages.html', messages=rows, search=search)

@app.route('/messages/delete/<int:id>', methods=['POST'])
def delete_message(id):
    if not session.get('admin'):
        return redirect(url_for('login'))
    conn = sqlite3.connect(DB_PATH)
    conn.execute('DELETE FROM messages WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('messages'))

init_db()

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', 'False') == 'True')
