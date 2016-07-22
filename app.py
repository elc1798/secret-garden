from flask import Flask, render_template, session, redirect, request, url_for
from functools import wraps
import db_session as dbs

app = Flask(__name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session or not session['logged_in'] \
                or "key" not in session:
            session.clear()
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def redirect_if_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session and session['logged_in']:
            return redirect(url_for("view"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
@app.route("/login/", methods=["GET", "POST"])
@redirect_if_logged_in
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        assert(request.method == "POST")
        password = request.form['pword']
        session['logged_in'] = True
        session['key'] = str(password)
        return redirect(url_for("view"))

@app.route("/view")
@app.route("/view/")
@login_required
def view():
    data = dbs.Session(session['key']).get_all()
    return render_template("view.html", DATA=data)

@app.route("/logout")
@app.route("/logout/")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.secret_key = "f307adee27943c759eb1e9c445952bd1"
    app.debug = True
    app.run('127.0.0.1', port=34567)


