from flask import Flask, render_template, request, session, redirect, url_for, g
import model

app = Flask(__name__)

# Placeholder secret key, to be replaced later
app.secret_key = "swordfish"

username = ""
user = model.check_users()

@app.route("/", methods = ["GET", "POST"])
def home():
    if "username" in session:
        g.user = session["username"]
        admin_message = ""
        if session["username"] == "chris":
            admin_message = "You're the admin"
        return render_template("mech.html", message = "<img src = static/img/8Hi2.gif>" + admin_message)
    return render_template("homepage.html", message = "Welcome!")
    


@app.before_request
def before_request():
    g.username = None
    if "username" in session:
        g.username = session["username"]

# adds path to the hosted page (localhost7000/mech)
@app.route("/mech", methods = ["GET"])
def mech():
        if "username" in session:
            g.user = session["username"]
            message = "<img src = static/img/8Hi2.gif>"
            admin_message = ""
            if session["username"] == "chris":
                admin_message = "You're the admin"
            else:
                message += f"<br> <br> {model.show_word(session['username'])} "

            return render_template("mech.html", message = message + admin_message)
        else:
            return render_template("homepage.html", message = "Welcome!")


@app.route("/login", methods = ["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        session.pop("username", None)
        areyouuser = request.form["username"]
        pwd = request.form["password"]
        if pwd == model.check_pass(areyouuser):
            session["username"] = request.form["username"]
            return redirect(url_for("mech"))
        else:
            # returns if login fails
            message = "Wrong Username or Password"
            return render_template("login.html", message = message)
        
        
    return render_template("login.html", message = message)
    


@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "GET":
        message = ""
        return render_template("signup.html", message = message)
    else:
        username = request.form["username"]
        password = request.form["password"]
        secret_word = request.form["secret_word"]
        message = model.signup(username, password, secret_word)
        return render_template("signup.html", message = message)

@app.route("/getsession")
def get_session():
    if username in session:
        return session["username"]
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000, debug = True)