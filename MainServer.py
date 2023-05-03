import mysql.connector

from API import app

# print(mysql.connector.__version__)

# Establish a connection to the MySQL server
db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="SmartWardrobe")

# Create a cursor object to execute queries
cursordb = db.cursor()

# Execute a SELECT query to retrieve all users' usernames and emails
query = "SELECT user.userName, user.email FROM user"
cursordb.execute(query)

# Fetch all the rows returned by the query
result = cursordb.fetchall()

# Print the username and email of each user
for row in result:
    print("Username:", row[0])
    print("Email:", row[1])

# Close the cursor and database connection
cursordb.close()
db.close()
