import sqlite3

# used to seed initial tables with test data

connection = sqlite3.connect("flask_tut.db", check_same_thread = False)
cursor = connection.cursor()

cursor.execute(

    """
    INSERT INTO users(
    username,
    password,
    secret_word
    )
    VALUES(
    'Bob',
    'pass',
    'buildIt'
    );
    """
)

connection.commit()
cursor.close()
connection.close()