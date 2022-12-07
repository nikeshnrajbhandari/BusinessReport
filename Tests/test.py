import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="12345")

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Executing an MYSQL function using the execute() method
# cursor.execute("select version()")

# # Fetch a single row using fetchone() method.
# data = cursor.fetchone()
# print("Connection established to: ",data)

# #Closing the connection
# conn.close()

cursor.execute('''SELECT * FROM TEST''')
#Fetching 1st row from the table
result = cursor.fetchone()
print(result)

#Fetching 1st row from the table
results = cursor.fetchall()
print(results)

#Commit your changes in the database
conn.commit()

#Closing the connection
conn.close()