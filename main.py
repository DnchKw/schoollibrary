import os
from random import randint

from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3 as sl
import bcrypt

app = Flask(__name__)
app.secret_key = "secretkey"

# MySQL Configuration
app.config['UPLOAD_FOLDER'] = 'static/images'
con = sl.connect('library.db', check_same_thread=False)
cur = con.cursor()

# class Articles():
    # 
    # id = cur.execute('SELECT id FROM books')
    # title = cur.execute('SELECT title FROM books')
    # author = cur.execute('SELECT author FROM books')
    # desc = cur.execute('SELECT description FROM books')
    # year = cur.execute('SELECT year FROM books')
    # count = cur.execute('SELECT count FROM books')

# Routes
@app.route('/')
def index():
    if 'loggedin' in session:
        return redirect(url_for('main'))
    else:
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'loggedin' in session:
        return redirect(url_for('main'))
    else:
        if request.method == 'POST':
            global username
            username = str(request.form['username'])
            password = str(request.form['password'])

            cur = con.cursor()
            cur.execute(f'SELECT * FROM users WHERE username == :username',
                        {'username': bytes(username, encoding='utf-8')})
            user = cur.fetchone()
            cur.close()
            if user and bcrypt.hashpw(bytes(password, encoding='utf8'), user[2]):
                session['loggedin'] = True
                session['id'] = user[0]
                session['username'] = user[1]
                return redirect(url_for('main'))
            else:
                error = "Incorrect username or password."
                return render_template('login.html', error=error)
        else:
            return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # get the form data
        username = request.form['username'].encode('utf8')
        password = request.form['password'].encode('utf8')
        confirm_password = request.form['confirm_password'].encode('utf8')

        # check if the passwords match
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('signup'))

        # check if the username is already taken
        cur = con.cursor()
        cur.execute(f'SELECT id FROM users WHERE username == :username', {'username': username})
        user = cur.fetchone()
        cur.close()
        if user:
            flash('Username is already taken.', 'danger')
            return redirect(url_for('signup'))

        # insert the new user into the database
        cur = con.cursor()
        cur.execute('INSERT INTO users (username, password)'
                    ' VALUES (:username, :password)', {'username': username,
                                                       'password': bcrypt.hashpw(password, bcrypt.gensalt())
                                                       })
        con.commit()
        cur.close()

        flash('You have successfully signed up. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'loggedin' in session:
        if request.method == 'POST':
            cur = con.cursor()
            title = request.form['hh']
            cur.execute(f"DELETE FROM books WHERE title == :title", {'title': title})
            con.commit()
            cur.close()
        cur = con.cursor()
        cur.execute("SELECT * FROM books")
        books = cur.fetchall()
        cur.close()
        return render_template('admin.html', books=books)
    else:
        return redirect(url_for('index'))


@app.route('/main', methods=['GET', 'POST'])
def main():
    if 'loggedin' in session:
        cur = con.cursor()
        if request.method == 'POST':
            # cur.execute("SELECT * FROM books WHERE title LIKE :search", {'search': f'%{request.form["search"]}%'})
            user = session.get('username').decode('utf8')
            title = request.form['title']
            author = request.form['author']
            image = request.form['image']
            count = request.form['count']
            count = int(count) - 1
            if count > -1:
                print({'user': user, 'title': title, 'author': author, 'image': image})
                cur.execute("INSERT INTO orders (users, title, author, image) VALUES " "(:user, :title, :author, :image)", {'user': user, 'title': title, 'author': author, 'image': image})
                cur.execute("UPDATE books SET count = :count WHERE title == :title", {'count': count, 'title': title})
                con.commit()
        # if request.method == 'POST':
        #     cur.execute("SELECT * FROM books WHERE title LIKE :search", {'search': f'%{request.form["search"]}%'})
        cur = con.cursor()
        cur.execute('SELECT * FROM books')
        books = cur.fetchall()
        cur.close()
        return render_template('main.html', books=books, count_book=len(books))
    else:
        return redirect(url_for('index'))


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if 'loggedin' in session:
        if request.method == 'POST':
            title = request.form['title']
            author = request.form['author']
            description = request.form['description']
            count = request.form['count']
            year = request.form['year']
            photo = request.files['photo']
            image_name = f'{randint(0, 255)}.jpg'
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], image_name))

            cur = con.cursor()
            print(                {'title': title,
                 'autor': author,
                 'year': year,
                 'description': description,
                 'image': image_name,
                 'count': int(count)})
            cur.execute(
                "INSERT INTO books (title, author, year, description, image, count) VALUES "
                "(:title, :author, :year, :description, :image, :count)",
                {'title': title,
                 'author': author,
                 'year': year,
                 'description': description,
                 'image': image_name,
                 'count': int(count)})
            con.commit()
            cur.close()

            return redirect(url_for('admin'))

        else:
            return render_template('add_book.html')
    else:
        return redirect(url_for('index'))





# @app.route('/<id>', methods=["GET"])
# def book_info(id):
#    if 'loggedin' in session:
#         # cur = con.cursor()
#         # # article = Articles.query.get(id)
#         # cur.execute(f"SELECT * FROM books WHERE title == :title", {'title': title})
#         # books = cur.fetchall()
#         # cur.close()
#         # return render_template('book_info.html', book=books)
#         book_id = request.form.get(id)

#         cur = con.cursor()
#         cur.execute(f'SELECT * FROM books WHERE id == :id',
#                     {'id': book_id})
#         books = cur.fetchone()
#         cur.close()
#         return render_template('book_info.html', book=book_id)
#    else:
#        return redirect(url_for('index'))


@app.route('/bag', methods=['GET', 'POST'])
def bag():
    if 'loggedin' in session:
        cur = con.cursor()
        user = session.get('username').decode('utf8')
        cur.execute(f'SELECT * FROM orders WHERE users == :users', {'users': user})
        order = cur.fetchall()
        cur.close()
        return render_template('bag.html', orders=order, count_order=len(order))
    else:
        return redirect(url_for('index'))

@app.route('/bag_clean', methods=['POST'])
def bag_clean():
    if 'loggedin' in session:
        if request.method == 'POST':
            cur = con.cursor()
            bId = request.form['id']
            title = request.form['title']
            cur.execute(f"DELETE FROM orders WHERE id == :id", {'id': bId})
            cur.execute(f'SELECT count FROM books WHERE title == :title', {'title': title})
            count = cur.fetchone()
            count = count[0] + 1
            cur.execute(f"UPDATE books SET count = :count WHERE title == :title", {'count': count, 'title': title})
            con.commit()
            cur.close()
        return redirect(url_for('bag'))
    else:
        return redirect(url_for('index'))


@app.route('/profile')
def profile():
    if 'loggedin' in session:
        user = session.get('username').decode('utf8')
                    

        return render_template('profile.html', user=user)
    else:
        redirect(url_for('index'))


@app.route('/ordes')
def orders():
    if 'loggedin' in session:
        cur = con.cursor()
        cur.execute('SELECT * FROM orders')
        orders = cur.fetchall()
        cur.close()
        return render_template('orders.html', orders=orders, count_orders=len(orders))
    else:
        return redirect(url_for('index'))

@app.route('/order_clear', methods=['POST'])
def order_clear():
    if 'loggedin' in session:
        if request.method == 'POST':
            cur = con.cursor()
            bId = request.form['oc']
            title = request.form['title']
            cur.execute(f"DELETE FROM orders WHERE id == :id", {'id': bId})
            cur.execute(f'SELECT count FROM books WHERE title == :title', {'title': title})
            count = cur.fetchone()
            count = count[0] + 1
            cur.execute(f"UPDATE books SET count = :count WHERE title == :title", {'count': count, 'title': title})
            con.commit()
            cur.close()
        return redirect(url_for('orders'))
    else:
        return redirect(url_for('index'))



@app.route('/TODO')
def todo():
    return render_template('TODO.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)
