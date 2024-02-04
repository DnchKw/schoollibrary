import sqlite3
c = sqlite3.connect('library.db')
<<<<<<< HEAD
c.execute('CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username VARCHAR(50), password VARCHAR(100));')
=======
c.execute('CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username VARCHAR(50), password VARCHAR(100));')
>>>>>>> main
