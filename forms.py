
import sqlite3

# returns HTML code forms with a total of 3 lines
# used to create multiple blank field to fill in
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