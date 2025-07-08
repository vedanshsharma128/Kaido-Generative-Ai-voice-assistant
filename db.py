import csv
import sqlite3

con = sqlite3.connect("kaido.db")
cursor = con.cursor()

# query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
# cursor.execute(query)


# # query = "INSERT INTO sys_command VALUES (null,'god of war', 'C:\\Games\\God of War\\GoW.exe')"
# # cursor.execute(query)
# # con.commit()

# query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO web_command VALUES (null,'drive', 'https://drive.google.com/drive/home')"
# cursor.execute(query)
# con.commit()


# testing module
# app_name = "android studio"
# cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
# results = cursor.fetchall()
# print(results[0][0])

# Create a table with the desired columns
cursor.execute('''CREATE TABLE IF NOT EXISTS contact (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')


# # Specify the column indices you want to import (0-based index)
# # Example: Importing the 1st and 3rd columns
# desired_columns_indices = [0, 20]

# # # Read data from CSV and insert into SQLite table for the desired columns
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#       csvreader = csv.reader(csvfile)
#       for row in csvreader:
#           selected_data = [row[i] for i in desired_columns_indices]
#           cursor.execute(''' INSERT INTO contact (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# # # Commit changes and close connection
# con.commit()
# con.close()
# Delete the contacts table
# cursor.execute("DROP TABLE IF EXISTS contacts")
# con.commit()

# print("The 'contacts' table has been deleted.")


# query = "INSERT INTO contacts VALUES (null,'mummy', '+91 8076919347', NULL)"
# cursor.execute(query)
# con.commit()

query = 'aksh'
query = query.strip().lower()

cursor.execute("SELECT mobile_no FROM contact WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
results = cursor.fetchall()

if results:
         print(results[0][0])
else:
    print("No results found for the given name.")

