from flask import Flask, render_template, request, session, redirect, flash
from flask_session import Session
import re
import string
from database import Database
from werkzeug.security import check_password_hash
from helpers import apology, login_required

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = Database('data/magazine_subscription.db')

def is_valid_title(title):
    if not (3 <= len(title) <= 30):
        return False
    if not re.match(r'^[A-Za-z0-9 ]+$', title):
        return False
    return True

EXEMPT_ROUTES = ['login', 'static']

@app.before_request
def require_login():
    if request.endpoint not in EXEMPT_ROUTES and "user_id" not in session:
        return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return apology("Missing username or password", 403)
        row = db.get_user(username)

        if not row or not check_password_hash(row["hash"], password):
            return apology("Missing username or password", 403)

        session["user_id"] = row["id"]
        return redirect("/")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('learnaboutme.html')

@app.route('/favourites')
def favourites():
    return render_template('myfavourites.html')

@app.route('/fact')
def fact():
    return render_template('fact.html')

@app.route('/contact')
def contact():
    return render_template('form.html')

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        reason = request.form.get('reason')
        password = request.form.get('password')
        message = request.form.get('message')
        subscribe = request.form.get('subscribe')

        return render_template('send.html')

    return render_template('form.html')

@app.route('/webweek3')
def webweek3():
    return render_template('webweek3.html')

@app.route('/project<int:num>')
def project(num):
    return render_template(f'project{num}.html')


@app.route('/validator', methods=['GET', 'POST'])
def validator():
    if request.method == 'POST':
        title = request.form['title']
        if is_valid_title(title):
            if not db.magazine_exists(title):
                db.add_numberMagazines(title)
                return render_template('magazine_checker/valid.html', magazine=title)
            else:
                return render_template('magazine_checker/invalid.html', message="This title already exists.")
        else:
            return render_template('magazine_checker/invalid.html', message="Title is invalid.")
    magazines = db.get_numberMagazines()
    return render_template('magazine_checker/checker.html', magazines=magazines)

if __name__ == "__main__":
    app.run(debug=True)
