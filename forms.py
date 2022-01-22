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


# returns HTML code forms with a total of 3 lines
# used to create multiple blank field to fill in
# name for forms are question + question number (eg, Question 3 = question3)
def set_question(num_of_questions):

    html_to_return = ""
    num = 0

    try:
        num = int(num_of_questions)
    except:
        num = 0

    for i in range(num):
        
        name = f"question{i+1}"
        print(name)
        #TODO - update name so form request accurately identifies field 
        #temporarly changed to "question" on name field for testing purposes 
        html_to_return += f"""
        <div class="mb-3">
        <label for="exampleFormControlTextarea1" class="form-label">Question {i + 1}</label>
        <textarea class="form-control" name="{name}" rows="3"></textarea>
        </div>
        """


    return html_to_return