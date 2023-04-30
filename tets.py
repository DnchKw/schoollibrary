import sqlite3
c = sqlite3.connect('library.db')
c.execute('CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50) NOT NULL, password VARCHAR(100) NOT NULL);')