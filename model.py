import sqlite3
from random import randint

def show_word(email):
    connection = sqlite3.connect("flask_tut.db", check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(
        f"""
        SELECT username
        FROM users
        WHERE email = '{email}';
        """
    )
    username = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    message = f"{email}'s username is \"{username}\"."
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