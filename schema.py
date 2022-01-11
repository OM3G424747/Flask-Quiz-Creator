import sqlite3

# used to create initial tables project

connection = sqlite3.connect("flask_tut.db", check_same_thread = False)
cursor = connection.cursor()

# Create User Table
cursor.execute(
    """
    CREATE TABLE users (
        id_num INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(255),
        email VARCHAR(255),
        pass VARCHAR(255),
        firstname VARCHAR(255),
        lastname VARCHAR(255),
        displayname BOOLEAN
    );
    """
)
connection.commit()
cursor.close()
connection.close()


connection = sqlite3.connect("flask_tut.db", check_same_thread = False)
cursor = connection.cursor()

# Create Quiz Table
cursor.execute(
    """
    CREATE TABLE quiz (
        quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_num INTEGER,
        quiz_name VARCHAR(255),
        total_questions INTEGER
    );
    """
)
connection.commit()
cursor.close()
connection.close()


connection = sqlite3.connect("flask_tut.db", check_same_thread = False)
cursor = connection.cursor()

# Create Question Table
cursor.execute(
    """
    CREATE TABLE question (
        question_id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER,
        questions_text VARCHAR(255),
        total_options INTEGER
    );
    """
)
connection.commit()
cursor.close()
connection.close()


connection = sqlite3.connect("flask_tut.db", check_same_thread = False)
cursor = connection.cursor()

# Create Answers Table
cursor.execute(
    """
    CREATE TABLE answers (
        question_id INTEGER,
        answer_text VARCHAR(255)
    );
    """
)
connection.commit()
cursor.close()
connection.close()



connection = sqlite3.connect("flask_tut.db", check_same_thread = False)
cursor = connection.cursor()

# Create Access Table
cursor.execute(
    """
    CREATE TABLE access (
        creator_id INTEGER,
        quiz_id INTEGER,
        testee_id INTEGER
    );
    """
)
connection.commit()
cursor.close()
connection.close()


connection = sqlite3.connect("flask_tut.db", check_same_thread = False)
cursor = connection.cursor()

# Create Score Table
cursor.execute(
    """
    CREATE TABLE score (
        quiz_id INTEGER,
        testee_id INTEGER,
        score INTEGER
    );
    """
)
connection.commit()
cursor.close()
connection.close()



