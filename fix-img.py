import sqlite3
c = sqlite3.connect('library.db')
#c.execute('ALTER books AUTOINCREMENT = 1')
c.execute('UPDATE books SET image = "171.jpg" WHERE title = "Живая Шляпа"')
c.execute('UPDATE books SET image = "153.jpg" WHERE title = "Алиса в стране чудес"')
c.execute('UPDATE books SET image = "emblema.png" WHERE title = "10М"')

c.commit()