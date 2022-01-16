import sqlite3
from random import randint

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


def set_question(num_of_questions):

    html_to_return = ""
    num = 0

    try:
        num = int(num_of_questions)
    except:
        num = 0

    for i in range(num):

        html_to_return += f"""
        <div class="mb-3">
        <label for="exampleFormControlTextarea1" class="form-label">Example textarea</label>
        <textarea class="form-control" name="test{i}" rows="3"></textarea>
        </div>
        """

    return html_to_return


def get_valid_num(num):

    cast_num = 0

    try:
        cast_num = int(num)
        if cast_num < 0: 
            cast_num = 0
        return cast_num
    
    except:
        return cast_num


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




#passes -1 as a quiz_id
#values of -1 indicate a query
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

    # writes initial active quiz
    if result == -1 and int(quiz_id) > 0:
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

    elif int(quiz_id) > 0:
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




# returns list of quizes available for editing
def get_selections(id_num):
    #sqlite> SELECT isadmin
    #...> FROM users
    #...> WHERE email = '{email}';
    connection = sqlite3.connect("flask_tut.db", check_same_thread = False)
    cursor = connection.cursor()
    
    result = ""
    cursor.execute(
        f"""
        SELECT quiz_id, quiz_name
        FROM quiz
        WHERE id_num = {id_num};
        """
    )
    try:
        result = cursor.fetchall()

    except:
        # returns negative 1 to indicate an error
        result = -1

    connection.commit()
    cursor.close()
    connection.close()

    selections = '<label for="exampleFormControlInput1" class="form-label">Select Quiz: </label>'
    selections += '<select name="test" onchange="this.form.submit();">'
    selections += "<option value=' '> </option>"


    for test in result:
        selections += f"<option value='{test[0]}'>{test[1]}</option>"

    selections += "</select>"

    return selections


def get_quiz_name(quiz_id):
    connection = sqlite3.connect("flask_tut.db", check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(
        f"""
        SELECT quiz_name
        FROM quiz
        WHERE quiz_id = '{quiz_id}';
        """
    )

    try:
        result = cursor.fetchone()[0]
    except:
        # returns negative 1 to indicate an error
        result = -1

    return result




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


