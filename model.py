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

    if result == -1:
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
    else:
        connection.commit()
        cursor.close()
        connection.close()
        return "Username already in use."

    connection.commit()
    cursor.close()
    connection.close()
    return "User registered successfully."




# used to sign up a new user
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
    
    try:
        result = cursor.fetchone()[0]
    except:
        # returns negative 1 to indicate an error
        result = -1

    if result == -1:
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
    else:
        connection.commit()
        cursor.close()
        connection.close()
        return "You already have a quiz with this name."

    connection.commit()
    cursor.close()
    connection.close()
    return "Quiz creatred successfully."



#passing only email indicates a query
#passes -1 as a quiz_id for default query to only return a result
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




# test for changing active quiz
#print(active_quiz("chris.joubert@mogi-group.com", 3))



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
    



#TODO continue here, convert into a function for populating page with correct number of questions

#SELECT total_questions
#FROM quiz
#WHERE quiz_id = {inset quiz ID here}

#TODO, INSERT questions to match the number selected!

#TODO, after initial insert, UPDATE

#CREATE TABLE question (
        #question_id INTEGER PRIMARY KEY AUTOINCREMENT,
        #quiz_id INTEGER,
        #questions_text VARCHAR(255),
        #total_options INTEGER

print(update_questions(1))