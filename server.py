from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import csv
import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

app = Flask(__name__)
print(__name__)

BASE_DIR = Path(__file__).resolve().parent
CONTACT_EMAIL = 'omosekeji88@gmail.com'


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'alien.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/index.html')
def index():
    return redirect(url_for('home'))


@app.route('/works.html')
def works():
    return render_template('works.html')


@app.route('/work.html')
def project_oct_atlas():
    return render_template('work.html')


@app.route('/about.html')
def about():
    return render_template('about.html')


@app.route('/contact.html')
def contact():
    return render_template('contact.html', submitted=request.args.get('submitted') == 'true')


@app.route('/thankyou.html')
def thankyou():
    return render_template('thankyou.html')


def write_to_txt(data):
    with (BASE_DIR / 'database.txt').open(mode='a', encoding='utf-8') as database:
        database.write(f"Email: {data.get('email', '')}\n")
        database.write(f"Subject: {data.get('subject', '')}\n")
        database.write(f"Message: {data.get('message', '')}\n")
        database.write("---\n")


def write_to_csv(data):
    csv_path = BASE_DIR / 'database.csv'
    file_is_empty = not csv_path.exists() or csv_path.stat().st_size == 0
    with csv_path.open(mode='a', newline='', encoding='utf-8') as database:
        writer = csv.DictWriter(database, fieldnames=['email', 'subject', 'message'])
        if file_is_empty:
            writer.writeheader()
        writer.writerow({
            'email': data.get('email', ''),
            'subject': data.get('subject', ''),
            'message': data.get('message', ''),
        })


def send_contact_email(data):
    password = os.environ.get('CONTACT_EMAIL_PASSWORD')
    if not password:
        print('Contact form saved, but email was not sent because CONTACT_EMAIL_PASSWORD is not set.')
        return False

    sender = os.environ.get('CONTACT_EMAIL_FROM', CONTACT_EMAIL)
    smtp_server = os.environ.get('CONTACT_SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('CONTACT_SMTP_PORT', '587'))

    message = EmailMessage()
    message['Subject'] = f"Portfolio contact form: {data.get('subject', 'New message')}"
    message['From'] = sender
    message['To'] = CONTACT_EMAIL
    message['Reply-To'] = data.get('email', '')
    message.set_content(
        f"From: {data.get('email', '')}\n"
        f"Subject: {data.get('subject', '')}\n\n"
        f"Message:\n{data.get('message', '')}\n"
    )

    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(sender, password)
        smtp.send_message(message)
    return True


@app.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.form.to_dict()
    write_to_txt(data)
    write_to_csv(data)
    try:
        email_sent = send_contact_email(data)
    except Exception as error:
        print(f'Contact email failed: {error}')
        email_sent = False
    return redirect(url_for('contact', submitted='true', emailed=str(email_sent).lower()))
