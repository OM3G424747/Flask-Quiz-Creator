import sqlite3

# returns list of quizes available for editing as HTML code to be displayed
def get_selections(id_num):

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