import sqlite3
from random import randint
import csv, os
import pandas as pd
from model import set_password



#lists file in selected directory
#file = open("")
path = "data_files/"

files = os.listdir(path)

# lists file names 
for f in files:
	print(f)
# opens the first file found
file = open(f"data_files/{files[0]}")
file.close()


# opens excel file and sets it as a dataframe 
full_file = pd.ExcelFile("data_files/agent_info.xlsx")

# selects specified worksheet in df and creats a new df with headers set to row 0
koa_df = pd.read_excel(full_file, "KoA - Agents Info", header = 0)


print(koa_df["End Date (d/m/y)"])


"""
email = Mogi/Dingtalk Email
password = get_password()
Name = Name
HS Name = HS Name
is_admin = 0
"""

# connects to SQL
connection = sqlite3.connect("flask_tut.db", check_same_thread = False)
cursor = connection.cursor()

cursor.execute(
    f"""
    SELECT email
    FROM users;
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

print(result)

connection.commit()
cursor.close()
connection.close()


#TODO continue HERE!!!!!!
#TODO update to loop over DF and upload the values needed 
row = 0
for i in koa_df["Name"]:
    # creates an agent object with the specified details 
    current_agent = koa_df.loc[row, "Name" : "HS Name" ]
    # print(current_agent["End Date (d/m/y)"])
    row += 1

    if current_agent["Mogi/Dingtalk Email"] not in result and current_agent["Status"] == "Active":
        print(f"Adding {current_agent['Name']} with status {current_agent['Status']}") 
        
        connection = sqlite3.connect("flask_tut.db", check_same_thread = False)
        cursor = connection.cursor()
        cursor.execute(

            f"""
            INSERT INTO users(
            email,
            password,
            name,
            hsname,
            isadmin
            )
            VALUES(
            '{current_agent['Mogi/Dingtalk Email']}',
            '{set_password()}',
            '{current_agent['Name']}',
            '{current_agent['HS Name']}',
            0
            );
            """
        )

        connection.commit()
        cursor.close()
        connection.close()
    
    else:
        print(f"{current_agent['Name']}, already in DB")










# convert into function that get's run if a new user is detected
"""
uniqueID = 0
for i in range(len(rows)):
    mycursor.execute("SELECT id FROM namedisplay")
    myresult = mycursor.fetchall()
    
    fullname = rows[i - 1][0].split(" ", 1)

    if uniqueID == 0:
        uniqueID = int(myresult[0][0]) + 1

    mycursor.execute(f"INSERT INTO namedisplay VALUES ({uniqueID}, \"{fullname[0]}\", \"{fullname[1]}\", \"{rows[i - 1][22]}\");")
    mycursor.execute(f"INSERT INTO username VALUES ({uniqueID}, \"{rows[i - 1][1]}\", \"{get_password()}\");")
    mycursor.execute(f"INSERT INTO accesskey VALUES ({uniqueID}, \"{get_password()}\");")
    print(f"Added {fullname} with {uniqueID}")
    uniqueID += 1

    mydb.commit()
"""




    #for x in mycursor:
        #print(x[-1])
"""
    mycursor.execute("INSERT INTO namedisplay VALUES (id, firstname, lastname, HSdisplayname);")
    mycursor.execute("INSERT INTO username VALUES (id, email, username);")
    mycursor.execute("INSERT INTO accesskey VALUES (id, password);")
"""



### open other file to load agent KPI data 
"""
print(files)

file = open(f"file_to_upload/{files[1]}", encoding="utf8")
csvreader = csv.reader(file)

header = []
header = next(csvreader)
# int number for header correlates with int number in rows for column

rows = []
for row in csvreader:
        rows.append(row)

# first int =  row
# second int = column

#0 = Agents
#1 = Agent Score
#2 = Issues Assigned
#3 = Issues Resolved
#4 = Average Survey Rating
#5 = Backlog
#6 = Time to First Response
#7 = Holding Time
#8 = Average Time to Resolve
#9 = Median Time to Resolve
#10 = Response Rate
#11 = Acceptance Rate
#12 = Reopens
#13 = Reopen Rate
#14 = Issues Rejected
#15 = Issues worked on
#16 = FCR Rate
#17 = Outbound Interactions
#18 = Resolved Without Response
#19 = Replies Per Resolve
#20 = Rating 1 Star
#21 = Rating 2 Star
#22 = Rating 3 Star
#23 = Rating 4 Star
#24 = Rating 5 Star


file.close()

# YYYY-MM-DD

# test = 
# colum 1 agents = is in "namedisplay table - displayname" = return ID
# add into CSAT table  - use date and ID as keys
# values to include = stars 


# date formatted: 
# 0 = MM 
# 1 = DD 
# 2 = YYYY
date = files[1][24:-17:1].split("_")

day = f"{date[2]}-{date[0]}-{date[1]}"
print(date)
print(rows[0][0])

hs_name_result = []
date_dict = {}
id_dict = {}

mycursor.execute("SELECT displayname FROM namedisplay")
results = mycursor.fetchall()

# create local list with current list on server
for i in range(len(results)):
    hs_name_result.append(results[i][0])


mycursor.execute(f"SELECT id, date FROM csat where date = '{date[2]}-{date[0]}-{date[1]}'")
results = mycursor.fetchall()
# create local dictionary to store daily data for checking 
for i in range(len(results)):
    date_dict[results[i][0]] = results[i][1]

mycursor.execute(f"SELECT id, displayname FROM namedisplay")
agent_id = mycursor.fetchall()

for i in range(len(agent_id)):
    print(agent_id[i][1])
    id_dict[agent_id[i][1]] = agent_id[i][0]

# checks if the current agent in on the server    
for i in range(len(rows)):

    # checks if name is on server and if the id and date are already registered for CSAT
    if rows[i][0] in hs_name_result and str(date_dict[id_dict[rows[i][0]]]) != day:
        print(f"{rows[i][0]} is on the server!" )
        print(f"1 Star {rows[i][20]}")
        print(f"2 Star {rows[i][21]}")
        print(f"3 Star {rows[i][22]}")
        print(f"4 Star {rows[i][23]}")
        print(f"5 Star {rows[i][24]}")
        mycursor.execute(f"SELECT id FROM namedisplay WHERE displayname = '{rows[i][0]}'")
        agent_id = mycursor.fetchall()
        print(agent_id[0][0])
        
        # adds CSAT to CSAT table
        mycursor.execute(f"INSERT INTO csat VALUES ({agent_id[0][0]}, '{date[2]}-{date[0]}-{date[1]}', {rows[i][20]}, {rows[i][21]}, {rows[i][22]}, {rows[i][23]}, {rows[i][24]});")
        mydb.commit()


    else:
        print(f"{rows[i][0]} skipped")


#TODO - next head to AWS Lamda and create a function to
# 1) - login
# 2) - display CSAT (inned join where ID matches login )

mycursor.execute("SELECT displayname FROM namedisplay WHERE displayname = 'BOB'")
results = mycursor.fetchall()
# results are empty of no results are return = "len is 0"
# use to check if date and id are already on CSAT table
# if table len > 0 = skip 
print(results)

#for x in myresult:
#    print(x)

#for i in range(len(rows)):
#    mycursor.execute("SELECT (id, date) FROM csat")
#    myresult = mycursor.fetchall()

#insert into csat values(777, \"{date[2]}-{date[0]}-{date[1]}\", 1, 2, 3, 4, 5 )#


# TODO - write a function that takes a username and password:
# the function checks if the username and password match (have same ID)
# if not the function returns flase and ID 0
# if true the function returns true and the ID

def get_id(username, password):
    mydb = mysql.connector.connect(
    host="test.cazr6gubvkba.us-east-2.rds.amazonaws.com",
    user="root",
    password="fuckedup",
    database="test"
    )

    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT id FROM username WHERE username = '{username}' OR email = '{username}'")
    results = mycursor.fetchall()
    
    user_id = 0
    if len(results) > 0:
        user_id = results[0][0]
        print(f"the ID is {results[0][0]}")

    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT id FROM accesskey WHERE pass = '{password}'")
    results = mycursor.fetchall()
    
    pass_id = 0
    if len(results) > 0:
        pass_id = results[0][0]
        print(f"the ID is {results[0][0]}")

    if user_id != 0 and pass_id != 0:
        if user_id == pass_id:
            print("Login successfull")
            return user_id

    else:
        print("Username and password do not match")
        return -1




print(get_id("chris.joubert@mogi-group.com","redSquirtle17"))

print(get_id("chris.joubert@mogi-group.com","blabla"))


"""

