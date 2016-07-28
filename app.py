from flask import Flask, render_template, session, redirect, request, url_for
from functools import wraps
import db_session as dbs

app = Flask(__name__)

current_session = None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session or not session['logged_in'] \
                or "key" not in session or current_session == None:
            session.clear()
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def redirect_if_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session and session['logged_in'] and current_session != None:
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
        global current_session
        current_session = dbs.Session(session['key'])
        return redirect(url_for("view"))

@app.route("/view")
@app.route("/view/")
@login_required
def view():
    global current_session
    data = current_session.get_all()
    return render_template("view.html", DATA=data)

@app.route("/add", methods=["GET", "POST"])
@app.route("/add/", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "GET":
        return render_template("add_new.html")
    else:
        assert(request.method == "POST")
        tkey = request.form['key']
        tuname = request.form['uname']
        tpword = request.form['pword']
        global current_session
        current_session.insert_into_table(tkey, tuname, tpword)
        return redirect(url_for("view"))

@app.route("/remove")
@app.route("/remove/")
@login_required
def remove():
    tkey = request.args.get('key')
    tuname = request.args.get('uname')
    global current_session
    current_session.remove_from_table(tkey, tuname)
    return redirect(url_for("view"))

@login_required
@app.route("/logout")
@app.route("/logout/")
def logout():
    session.clear()
    current_session = None
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.secret_key = "f307adee27943c759eb1e9c445952bd1"
    app.debug = True
    app.run('127.0.0.1', port=34567)


