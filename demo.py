from flask import Flask, render_template, request, session, redirect, url_for, g
import model, forms

app = Flask(__name__)

# TODO - Placeholder secret key, to be replaced later
app.secret_key = "swordfish"

username = ""
user = model.check_users()
test = ""

# homepage
@app.route("/", methods = ["GET", "POST"])
def home():
    if "username" in session:
        g.user = session["username"]
        admin_message = ""
        if session["username"] == "chris":
            admin_message = "You're the admin"
        return render_template("dashboard.html", message = "<img src = static/img/8Hi2.gif>" + admin_message)
    return render_template("homepage.html", message = "Welcome!")
    

# confirms the user is corrently signed in
@app.before_request
def before_request():
    g.username = None
    if "username" in session:
        g.username = session["username"]


# main dashboard of the signed in user 
@app.route("/dashboard", methods = ["GET"])
def dashboard():
        if "username" in session:
            g.user = session["username"]
            message = "<img src = static/img/8Hi2.gif>"

            user_id = model.get_id(g.user)
            
            button = ""
            # creates a new button after the user creates their first quiz
            if model.has_created( user_id ) != -1:
                button = """
                    <a href="/quizsetup">
                    <button class="w-100 btn btn-lg btn-primary" id="floatingInput">Edit Quiz</button>
                    </a>
                    """

            return render_template("dashboard.html", message = message, button = button)
        else:
            return render_template("homepage.html", message = "Welcome!")


# adds a new quiz under the signed in user 
@app.route("/newquiz", methods = ["GET", "POST"])
def newquiz():
        if "username" in session:
            g.user = session["username"]
            user_id = model.get_id(g.user)
            
            # sets the number of questions to a static number of 2
            message = ""

            button = ""
            # creates a new button after the user creates their first quiz
            if model.has_created( user_id ) != -1:
                button = """
                    <a href="/quizsetup">
                    <button class="w-100 btn btn-lg btn-primary" id="floatingInput">Edit Quiz</button>
                    </a>
                    """


            if request.method == "POST":
                
                user_id = model.get_id(g.user)
                quiz_name = request.form["testname"]
                question_num = request.form["number"]

                message = model.createquiz(user_id, quiz_name, question_num)

                if model.has_created( user_id ) != -1:
                    button = """
                        <a href="/quizsetup">
                        <button class="w-100 btn btn-lg btn-primary" id="floatingInput">Edit Quiz</button>
                        </a>
                        """
                

            return render_template("newquiz.html", message = message, button = button)
        else:
            return render_template("homepage.html", message = "Welcome!")



# page for setting up the questions in the the selected quiz
@app.route("/quizsetup", methods = ["GET", "POST"])
def quizsetup():
        if "username" in session:
            g.user = session["username"]
            
            message = ""
            quiz_id = model.active_quiz(g.user)
            user_id = model.get_id(g.user)
            
            # defaults rendered quiz to first quiz on user's list
            if quiz_id == -1:
                quiz_id = model.get_quiz_id(user_id)[0][0]
            
            # replace int with number of questions user selected for specific quiz
            total_questions = model.get_total_questions(quiz_id)
            questions = forms.set_question(total_questions)
            
            # displays the selection of available quizes for the user
            quiz_name = model.get_quiz_name(quiz_id)

            selection = forms.get_selections(user_id, quiz_name)
            
            if quiz_name != -1:
                message = f"<h3>Now editing:<br> <u><strong>{quiz_name}<br>Total Questions:{total_questions}</strong></u></h3>"


            if request.method == "GET":
                quiz_id = model.active_quiz(g.user)

            # updates page to displays the users' selection
            # also update DB with users' data
            else:

                # access before updating quiz_id
                for i in range(total_questions):
                    print
                    print( f"this is the result { request.form[f'question{i+1}'] } " )

                # accessing updates quiz id and changes the value of "total_questions"
                quiz_id = request.form['test']
                
                # displays the selection of available quizes for the user
                quiz_name = model.get_quiz_name(quiz_id)

                selection = forms.get_selections(user_id, quiz_name)

                #updates selected quiz for next render
                model.active_quiz(g.user, quiz_id)
                quiz_name = model.get_quiz_name(quiz_id)
                # replace int with number of questions user selected for specific quiz
                total_questions = model.get_total_questions(quiz_id)
                questions = forms.set_question(total_questions)
                # message to be displayed at top of page as a header
                message = f"<h3>Now editing:<br> <u><strong>{quiz_name}<br>Total Questions:{total_questions}</strong></u></h3>"

            return render_template("quizsetup.html", selection = selection , message = message, questions = questions)

        else:
            return render_template("homepage.html", message = "Welcome!")

# login page for users to login
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
    

# sign up page for creating a new user 
@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "GET":
        message = ""
        return render_template("signup.html", message = message)
    else:
        username = request.form["username"]
        
        #TODO - update to not accept blank passowrds
        password = request.form["password"]
        email = request.form["email"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]

        try:
            displayname = request.form["displayname"]

        except:
            displayname = "False"

        message = model.signup(username, password, email, firstname, lastname, displayname)
        return render_template("signup.html", message = message)

# confirms if the user has an active session 
@app.route("/getsession")
def get_session():
    if username in session:
        return session["username"]
    return redirect(url_for("login"))

# logout the current user 
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))

# sets the localhost port
if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000, debug = True)