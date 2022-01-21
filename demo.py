from flask import Flask, render_template, request, session, redirect, url_for, g
import model, forms

app = Flask(__name__)

# TODO - Placeholder secret key, to be replaced later
app.secret_key = "swordfish"

username = ""
user = model.check_users()
test = ""

@app.route("/", methods = ["GET", "POST"])
def home():
    if "username" in session:
        g.user = session["username"]
        admin_message = ""
        if session["username"] == "chris":
            admin_message = "You're the admin"
        return render_template("dashboard.html", message = "<img src = static/img/8Hi2.gif>" + admin_message)
    return render_template("homepage.html", message = "Welcome!")
    


@app.before_request
def before_request():
    g.username = None
    if "username" in session:
        g.username = session["username"]

# adds path to the hosted page (localhost7000/dashboard)
@app.route("/dashboard", methods = ["GET"])
def dashboard():
        if "username" in session:
            g.user = session["username"]
            message = "<img src = static/img/8Hi2.gif>"
            admin_message = ""
            if session["username"] == "chris":
                admin_message = "You're the admin"
            else:
                message += f" "

            return render_template("dashboard.html", message = message + admin_message)
        else:
            return render_template("homepage.html", message = "Welcome!")


# adds path to the hosted page (localhost7000/dashboard)
@app.route("/newquiz", methods = ["GET", "POST"])
def newquiz():
        if "username" in session:
            g.user = session["username"]
            
            # sets the number of questions to a static number of 2
            message = ""

            if request.method == "POST":
                
                #number = model.get_valid_num(request.form["number"])
                #if number >= 1:
                user_id = model.get_id(g.user)
                quiz_name = request.form["testname"]
                question_num = request.form["number"]

                message = model.createquiz(user_id, quiz_name, question_num)
                

            return render_template("newquiz.html", message = message)
        else:
            return render_template("homepage.html", message = "Welcome!")



@app.route("/quizsetup", methods = ["GET", "POST"])
def quizsetup():
        if "username" in session:
            g.user = session["username"]
            
            message = ""
            quiz_id = model.active_quiz(g.user)
            user_id = model.get_id(g.user)
            
            # displays the selection of available quizes for the user
            selection = forms.get_selections(user_id)
            quiz_name = model.get_quiz_name(quiz_id)
            total_questions = model.get_total_questions(quiz_id)

            # replace int with number of questions user selected for specific quiz
            questions = forms.set_question(total_questions) 

            if quiz_name != -1:
                message = f"<h3>Now editing:<br> <u><strong>{quiz_name}</strong></u></h3>"


            if request.method == "GET":
                quiz_id = model.active_quiz(g.user)

            else:

                quiz_id = request.form['test']

                for i in range(total_questions):
                    print(request.form['question1'])

                #updates selected quiz for next render
                model.active_quiz(g.user, quiz_id)
                quiz_name = model.get_quiz_name(quiz_id)
                message = f"<h3>Now editing:<br> <u><strong>{quiz_name}</strong></u></h3>"

            return render_template("quizsetup.html", selection = selection , message = message, questions = questions)

        else:
            return render_template("homepage.html", message = "Welcome!")


@app.route("/login", methods = ["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        session.pop("username", None)
        areyouuser = request.form["email"]
        pwd = request.form["password"]
        if pwd == model.check_pass(areyouuser):
            session["username"] = request.form["email"]
            return redirect(url_for("dashboard"))
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
        email = request.form["email"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        displayname = request.form["displayname"]

        message = model.signup(username, password, email, firstname, lastname, displayname)
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