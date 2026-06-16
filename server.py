from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import csv
from pathlib import Path

app = Flask(__name__)
print(__name__)

BASE_DIR = Path(__file__).resolve().parent


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


@app.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.form.to_dict()
    write_to_txt(data)
    write_to_csv(data)
    return redirect(url_for('contact', submitted='true'))
