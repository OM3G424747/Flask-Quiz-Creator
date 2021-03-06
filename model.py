from ast import Not
import sqlite3
from random import randint

# checks if the passed value is:
# - a number
# - greater than 0
# - values less than 0 default to 0 
def get_valid_num(num):

    cast_num = 0

    try:
        cast_num = int(num)
        if cast_num < 0: 
            cast_num = 0
        return cast_num
    
    except:
        return cast_num



# generates a random password
# used for first time account creation
# used for password resets 
def set_password():

    colour_list = ["Red", "Yellow", "Blue", "Brown", 
                    "Orange", "Green", "Violet", "Black", 
                    "Carnation", "white", "Dandelion", "Cerulean", 
                    "Apricot", "Scarlet", "Teal", "Indigo", "Gray"]

    pokemon_list = ["Bulbasaur", "Ivysaur", "Venusaur", "Charmander",
                    "Charmeleon", "Charizard", "Squirtle", "Wartortle",
                    "Blastoise", "Caterpie", "Metapod", "Butterfree",
                    "Weedle", "Kakuna", "Beedrill", "Pidgey",
                    "Pidgeotto", "Pidgeot", "Rattata", "Raticate",
                    "Spearow", "Fearow", "Ekans", "Arbok",
                    "Pikachu", "Raichu", "Sandshrew", "Sandslash",
                    "Nidoran", "Nidorina", "Nidoqueen", "Nidoran",
                    "Nidorino", "Nidoking", "Clefairy", "Clefable", 
                    "Vulpix", "Ninetales", "Jigglypuff", "Wigglytuff",
                    "Zubat", "Golbat", "Oddish", "Gloom",
                    "Vileplume", "Paras", "Parasect", "Venonat",
                    "Venomoth", "Diglett", "Dugtrio", "Meowth",
                    "Persian", "Psyduck", "Golduck", "Mankey", 
                    "Primeape", "Growlithe", "Arcanine", "Poliwag",
                    "Poliwhirl", "Poliwrath", "Abra", "Kadabra", 
                    "Alakazam", "Machop", "Machoke", "Machamp", 
                    "Bellsprout", "Weepinbell", "Victreebel", "Tentacool", 
                    "Tentacruel", "Geodude", "Graveler", "Golem",
                    "Ponyta", "Rapidash", "Slowpoke", "Slowbro",
                    "Magnemite", "Magneton", "Doduo", "Dodrio", 
                    "Seel", "Dewgong", "Grimer", "Muk",
                    "Shellder", "Cloyster", "Gastly", "Haunter",
                    "Gengar", "Onix", "Drowzee", "Hypno",
                    "Krabby", "Kingler", "Voltorb", "Electrode", 
                    "Exeggcute", "Exeggutor", "Cubone", "Marowak",
                    "Hitmonlee", "Hitmonchan", "Lickitung", "Koffing",
                    "Weezing", "Rhyhorn", "Rhydon", "Chansey",
                    "Tangela", "Kangaskhan", "Horsea", "Seadra",
                    "Goldeen", "Seaking", "Staryu", "Starmie",
                    "Scyther", "Jynx", "Electabuzz", "Magmar",
                    "Pinsir", "Tauros", "Magikarp", "Gyarados",
                    "Lapras", "Ditto", "Eevee", "Vaporeon",
                    "Jolteon", "Flareon", "Porygon", "Omanyte",
                    "Omastar", "Kabuto", "Kabutops", "Aerodactyl",
                    "Snorlax", "Articuno", "Zapdos", "Moltres",
                    "Dratini", "Dragonair", "Dragonite", "Mewtwo",
                    "Mew"]

    password = colour_list[randint(0,len(colour_list)-  1)] 
    password += pokemon_list[randint(0,len(pokemon_list)-  1)]
    password += str(randint(1, 100))

    return password


# returs the user id of the selected email 
def get_id(email):
    connection = sqlite3.connect("flask_tut.db", check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(
        f"""
        SELECT id_num
        FROM users
        WHERE email = '{email}';
        """
    )
    username = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    message = username
    return message


# confirms if the correct password was entered 
def check_pass(email):
    connection = sqlite3.connect("flask_tut.db", check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(
        f"""
        SELECT pass
        FROM users
        WHERE email = '{email}';
        """
    )

    try:
        result = cursor.fetchone()[0]
    except:
        # returns negative 1 to indicate an error
        result = -1

    connection.commit()
    cursor.close()
    connection.close()

    return result


# returns a list for all current emails 
def check_users():
    connection = sqlite3.connect("flask_tut.db", check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(
        f"""
        SELECT email
        FROM users
        ORDER BY email DESC;
        """
    )

    try:
        db_users = cursor.fetchall()
        result = []

        for i in range(len(db_users)):
            user = db_users[i][0]
            result.append(user)

    except:
        # returns negative 1 to indicate an error
        result = -1

    connection.commit()
    cursor.close()
    connection.close()

    return result


# used to sign up a new user
# TODO - include conditions to check password as not being blank
def signup(username, password, email, firstname, lastname, displayname):
    connection = sqlite3.connect("flask_tut.db", check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(
        f"""
        SELECT username
        FROM users
        WHERE username = '{username}';
        """
    )
    
    try:
        result = cursor.fetchone()[0]
    except:
        # returns negative 1 to indicate an error
        result = -1

    is_blank = False
    if not (len(username.strip())):
        is_blank = True
    
    if not (len(password.strip())):
        is_blank = True

    if not (len(firstname.strip())):
        is_blank = True

    if not (len(lastname.strip())):
        is_blank = True

    if not (len(email.strip())):
        is_blank = True


    if result == -1 and not is_blank:
        cursor.execute(
        f"""
        INSERT INTO users(
        username,
        email,
        pass,
        firstname,
        lastname,
        displayname

        )
        VALUES(
        '{username}',
        '{email}',
        '{password}',
        '{firstname}',
        '{lastname}',
        {displayname}
        );
        """
        )
    
    elif is_blank:
        return "Fields cannot be left blank."
    
    else:
        connection.commit()
        cursor.close()
        connection.close()
        return "Username already in use."

    connection.commit()
    cursor.close()
    connection.close()
    return "User registered successfully."



# used to create a new quiz
def createquiz( id_num, quiz_name, total_questions):
    connection = sqlite3.connect("flask_tut.db", check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(
        f"""
        SELECT quiz_name
        FROM quiz
        WHERE id_num = {id_num} AND quiz_name = '{quiz_name}';
        """
    )
    

    #TODO troubleshoot bug here preventing new tests for being created on nginx server
    try:
        result = cursor.fetchone()[0]
    except:
        # returns negative 1 to indicate an error
        result = -1

    is_blank = False
    if not (len(quiz_name.strip())):
        is_blank = True
    
    if not (len(total_questions.strip())):
        is_blank = True

    if result == -1 and not is_blank:
        cursor.execute(
        f"""
        INSERT INTO quiz(
        id_num,
        quiz_name,
        total_questions
        )

        VALUES(
        {id_num},
        '{quiz_name}',
        {total_questions}
        );
        """
        )
    
    elif is_blank:
        return "Please enter a name and number of questions"
    
    else:
        connection.commit()
        cursor.close()
        connection.close()
        return "You already have a quiz with this name."

    connection.commit()
    cursor.close()
    connection.close()
    return "Quiz creatred successfully."


# used to query quizes created by the active user
# passing only email indicates a query
# passes -1 as a quiz_id for default query to only return a result
def active_quiz(email, quiz_id = -1):

    user_id = get_id(email)

    connection = sqlite3.connect("flask_tut.db", check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(
        f"""
        SELECT quiz_id
        FROM active_test
        WHERE id_num = {user_id};
        """
    )
    
    try:
        result = cursor.fetchone()[0]
    except:
        # returns negative 1 to indicate an error
        result = -1

    # writes initial active quiz if no active quiz is listed yet
    if result == -1 and int(quiz_id) >= 0:
        cursor.execute(
        f"""
        INSERT INTO active_test(
        id_num,
        quiz_id
        )
        VALUES(
        {user_id},
        {quiz_id}
        );
        """
        )

    elif result != -1 and int(quiz_id) >= 0:
        cursor.execute(
        f"""
        UPDATE active_test
        SET quiz_id = {quiz_id}
        WHERE id_num = {user_id};
        """
        )

    else:
        connection.commit()
        cursor.close()
        connection.close()
        return result

    connection.commit()
    cursor.close()
    connection.close()
    return quiz_id


# user to return the name of the quiz associated with the quiz id
def get_quiz_name(quiz_id):
    connection = sqlite3.connect("flask_tut.db", check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(
        f"""
        SELECT quiz_name
        FROM quiz
        WHERE quiz_id = {quiz_id};
        """
    )

    try:
        result = cursor.fetchone()[0]
    except:
        # returns negative 1 to indicate an error
        result = -1
    connection.commit()
    cursor.close()
    connection.close()

    return result


# user to return the number of total questions associated with the quiz id
def get_total_questions(quiz_id):
    connection = sqlite3.connect("flask_tut.db", check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(
        f"""
        SELECT total_questions
        FROM quiz
        WHERE quiz_id = {quiz_id};
        """
    )

    try:
        result = cursor.fetchone()[0]
    except:
        # returns negative 1 to indicate an error
        result = -1
    connection.commit()
    cursor.close()
    connection.close()

    return result


#1) - confirm if questions are present
#2) - if questions don't exist, add them for the number needed for that quiz
#3) - if the questions do exist, confirm the number matches the number for the quiz
#4) - if they don't match ADD / REMOVE 

# function user to update DB with 
# total number of questions to be displayed
def update_questions(quiz_id):

    connection = sqlite3.connect("flask_tut.db", check_same_thread = False)
    cursor = connection.cursor()
    
    # gets total question value for selected quiz
    cursor.execute(
        f"""
        SELECT total_questions
        FROM quiz
        WHERE quiz_id = {quiz_id};
        """
    )

    try:
        q_num = cursor.fetchone()[0]
    except:
        # returns negative 1 to indicate an error
        q_num = -1
    
    # test if questions are added for selected quiz yet
    cursor.execute(
        f"""
        SELECT question_id
        FROM question
        WHERE quiz_id = {quiz_id};
        """
    )

    try:
        q_array = cursor.fetchall()
    except:
        # returns negative 1 to indicate an error
        q_array = -1

    # if no questions are added yet, questions are added
    # default value for question text is set to none
    if q_array == -1:
        for i in range(q_num):
            cursor.execute(
                f"""
                INSERT INTO question(
                quiz_id,
                question_text,
                total_options
                )
                VALUES(
                {quiz_id},
                'NONE',
                {i + 1}
                )
                """
            )
    else:
        print("Already added")

# TODO - add section to test if number of questions match the total that should be there
# for example, remove questions if the user changed the total from 12 to 10
# or add default questions if the user selected to add more

    connection.commit()
    cursor.close()
    connection.close()
    

def has_created( user_id ):
    connection = sqlite3.connect("flask_tut.db", check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(
        f"""
        SELECT quiz_name
        FROM quiz
        WHERE id_num = {user_id};
        """
    )

    try:
        result = cursor.fetchone()[0]
    except:
        # returns negative 1 to indicate an error
        result = -1
    
    return result



# used to return a list of all quizes created by the user
def get_quiz_id( id_num ):
    connection = sqlite3.connect("flask_tut.db", check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(
        f"""
        SELECT quiz_id
        FROM quiz
        WHERE id_num = {id_num};
        """
    )

    try:
        result = cursor.fetchall()
    except:
        # returns negative 1 to indicate an error
        result = -1
    return result


#TODO continue here, convert into a function for populating page with correct number of questions

#SELECT total_questions
#FROM quiz
#WHERE quiz_id = {inset quiz ID here}

#TODO, INSERT questions to match the number selected!

#TODO, after initial insert, UPDATE


# returns a dictionary contain question IDs
# question IDs are indexed starting from 0
def get_question_id( quiz_id ):
    connection = sqlite3.connect("flask_tut.db", check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(
        f"""
        SELECT question_id
        FROM question
        WHERE quiz_id = {quiz_id};
        """
    )

    try:
        result = cursor.fetchall()
        dict_to_return = {}
        for i in range(len(result)):
            dict_to_return[i] = result[i][0]
        
        return dict_to_return


    except:
        # returns negative 1 to indicate an error
        result = -1
        return result


# retrieves array of IDs for questions of active quiz
def set_question( quiz_id, questions_text, total_options, id_dict, active_question ):
    

    #TODO - check array and append value to dictionary
    #check with active question
    #if active question value is not in dictionary, insert instead of update
    
    #TODO! - after adding option to delete questions
    #if more values are left than there should be, DELETE
    print(len(id_dict))

    connection = sqlite3.connect("flask_tut.db", check_same_thread = False)
    cursor = connection.cursor()

    if len(id_dict) > 0 and active_question <= len(id_dict):

        cursor.execute(
            f"""
            UPDATE question
            SET questions_text = {questions_text},
            total_options = {total_options}
            WHERE question_id = {id_dict[active_question]};
            """
            )
    
    elif active_question > len(id_dict):

        connection = sqlite3.connect("flask_tut.db", check_same_thread = False)
        cursor = connection.cursor()
        cursor.execute(
            f"""
            INSERT INTO question(
            quiz_id,
            questions_text,
            total_options
            )
            VALUES(
            {quiz_id},
            '{questions_text}',
            {total_options}
            );
            """
        )

    connection.commit()
    cursor.close()
    connection.close()



#CREATE TABLE question (
        #question_id INTEGER PRIMARY KEY AUTOINCREMENT,
        #quiz_id INTEGER,
        #questions_text VARCHAR(255),
        #total_options INTEGER




dict_test = {1:"test", 2:"test2", 3:"test3"}

print(len(dict_test))

for i in range(len(dict_test)):
    print(i)