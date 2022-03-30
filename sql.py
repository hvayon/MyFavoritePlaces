import sqlite3
connection = sqlite3.connect('shows.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE Places (
    ChatID int,
    Name varchar(255),
    Image varchar(255),
    latitude float,
    longitude float
)''')
connection.commit()
connection.close()