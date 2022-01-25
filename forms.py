import sqlite3

# returns list of quizes available for editing as HTML code to be displayed
def get_selections(id_num, active_quiz):

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

    for test in result:

        
        if test[1] == active_quiz:
            selections += f"<option value='{test[0]}' selected>{test[1]}</option>"

        else:
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
        
        # sets name for question field
        q_name = f"question{i+1}"

        # sets name for question drop down selection
        opt_name = f"edit{i+1}"
        
        html_to_return += f"""
        <div class="mb-3">
        <label for="exampleFormControlTextarea1" class="form-label">Question {i + 1}</label>
        <textarea class="form-control" name="{q_name}" rows="3"></textarea>
        <br>
        <label for="exampleFormControlInput1" class="form-label">Answer Type: </label>
        <select name="{opt_name}">
        <option value='True'>True or False</option>
        <option value='False'>1 to 5 scale</option>
        </select>
        </div>
        <br>
        """

        # TODO - include HTML for user options per question
        # for example - "True or Flase questions?"


    return html_to_return


