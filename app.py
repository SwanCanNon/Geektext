from flask import Flask, flash, render_template, redirect, make_response, request, url_for, session, jsonify, Response, json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField
from wtforms.validators import InputRequired, Email, Length, DataRequired
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required, current_user
from settings import *
import os

app.config['SECRET_KEY'] = 'secret'
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:YES@localhost/geek_text"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:aa09@localhost/geek_text"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://bce5ce263e3ba7:1543b1ce@us-cdbr-iron-east-02.cleardb.net/heroku_e86cfb095c1e8fa"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

book_copies = db.Table('book_copies',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
                       )

login_manager = LoginManager()
login_manager.init_app(app)

books = [
    {
        'name': 'Harry Potter',
        'price': 7.99,
        'isbn': 10,
        'rating': 2,
        'comments': 'Hi'
    },
    {
        'name': 'Game of Thrones',
        'price': 17.99,
        'isbn': 20,
        'rating': 2,
        'comments': 'Bye'
    }
]


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class RegistrationForm(FlaskForm):
    username = StringField('name', [validators.Length(min=4, max=25)])
    email = StringField('email', [validators.Length(min=6, max=35)])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message="Passwords must match")
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired])
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=4, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    password = db.Column(db.String(128))
    books = db.relationship('Book', secondary=book_copies, backref=db.backref('users', lazy='dynamic'))
    user_cards = db.relationship('UserCard', backref='user')
    user_shippings = db.relationship('UserShipping', backref='user')

    physical_address = db.Column(db.String(128))
    def __str__(self):
        return self.name


class UserCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.id'))
    CreditCardNum = db.Column(db.String(128))
    ExpMonth = db.Column(db.Integer)
    ExpYear = db.Column(db.Integer)
    CVS = db.Column(db.Integer)
    NameOnCard = db.Column(db.String(128))


class UserShipping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.id'))
    ShippingAddr = db.Column(db.String(128))
    ShippingCity = db.Column(db.String(128))
    ShippingState = db.Column(db.String(128))
    ShippingZip = db.Column(db.String(128))


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(128))
    title = db.Column(db.String(128))
    description = db.Column(db.String(128))
    price = db.Column(db.Float)
    authorName = db.Column(db.String(50))
    publisher = db.Column(db.String(128))
    genre = db.Column(db.String(32))

    def __str__(self):
        return f"{self.title}"


class Authors(db.Model):
    AuthorID = db.Column(db.Integer, primary_key=True)
    AuthorName = db.Column(db.String(50))
    AuthorBio = db.Column(db.String(10000))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('book.id'))


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    quantity = db.Column(db.Integer)

    def __str__(self):
        book = Book.query.get(self.book_id)
        return f"{book.title}"


class Saveforlater(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))

    def __str__(self):
        book = Book.query.get(self.book_id)
        return f"{book.title}"


@app.route('/', methods=['GET', 'POST'])
def real_index():
    return redirect(url_for('index'))


@app.route('/books', methods=['GET', 'POST'])
def index():
    books = Book.query.all()
    authors = Authors.query.all()
    print(authors)
    for author in authors:
        print(author.AuthorID)
        print(author.AuthorName)
        print(author.AuthorBio)

    print(books)

    for book in books:
        print(book.title)
        print(book.description)
        print(book.price)
    return render_template('books.html', books=books)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=form.name.data).first()
            if user and (user.password == form.password.data):
                login_user(user, remember=form.remember.data)
                print(current_user.name)
                flash("You are now logged in", 'success')
                return redirect(url_for('index'))
            else:
                flash("That username could not be found/password/username are incorrect", 'error')

    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out", 'success')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == "POST":
        # access the username, password, email 
        # access the db object and create new user 
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # check if a user already exists 
        #  with that username 
        exists = db.session.query(User.id).filter_by(name=username).scalar() is not None

        if exists == True:
            # session flash that someone already exists with that username
            flash("Someone already exists with that username", 'error')
            return redirect(url_for('register'))
        else:
            # create a new user with that password and username
            # and email 
            new_user = User(name=username, password=password, email=email)
            # in the homepage show a flask message saying 
            # you are now registered 
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
            # redirect them to the homepage 
            # session['user'] = request.form['username']

            flash("You were successfully registered", 'success')
            return redirect(url_for("index"))

    return render_template('register.html', form=form)


@app.route('/user_profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    print("current user in user profile function " + current_user.name)
    if current_user.is_authenticated:
        # current_user_id = current_user.get_id()
        # current_user = User.query.filter_by(id=current_user_id).first()
        user_shippings = current_user.user_shippings
        user_cards = current_user.user_cards

    if request.method == 'POST':
        user_db = User.query.filter_by(id=current_user.id).first()
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        physical_address = request.form['physical_address']
        current_user.name = name 
        current_user.email = email 
        current_user.password = password 
        current_user.physical_address = physical_address
        user_db.name = name 
        user_db.email = email 
        user_db.password = password 
        user_db.physical_address = physical_address
        db.session.commit()
        flash('successfully updated', 'success')
        return redirect(url_for('user_profile'))

    return render_template('user_profile.html', user_shippings=user_shippings, user_cards=user_cards)


@app.route('/add_user_card', methods=['GET', 'POST'])
def add_user_card():
    if request.method == 'POST':
        user_id = current_user.id 
        credit_card_num = request.form['CreditCardNum']
        expMonth = request.form['ExpMonth']
        expYear = request.form['ExpYear']
        cvs = request.form['CVS']
        nameOnCard = request.form['NameOnCard']
        new_card = UserCard(UserID=user_id, CreditCardNum=credit_card_num, ExpMonth=expMonth, ExpYear=expYear, CVS=cvs,
                            NameOnCard=nameOnCard)
        db.session.add(new_card)
        db.session.commit()
        flash('new card succesfully added', 'success')
        return redirect(url_for('user_profile'))

    return render_template('add_user_card.html')


@app.route('/add_user_shipping', methods=['GET', 'POST'])
def add_user_shipping():
    if request.method == 'POST':
        UserID = 1
        ShippingAddr = request.form['ShippingAddr']
        ShippingCity = request.form['ShippingCity']
        ShippingState = request.form['ShippingState']
        ShippingZip   = request.form['ShippingZip']
        new_user_shipping = UserShipping(UserID=UserID,ShippingAddr=ShippingAddr,ShippingCity=ShippingCity,ShippingState=ShippingState,ShippingZip=ShippingZip)
        db.session.add(new_user_shipping)
        db.session.commit()
        flash('new shipping succesfully added', 'success')
        return redirect(url_for('user_profile'))

    return render_template('add_user_shipping.html')


@app.route('/user_profile/edit_user_card/<int:id>', methods=['GET', 'POST'])
def edit_user_card(id):
    user_card = UserCard.query.filter_by(id=id).first()
    if request.method == 'POST':
         user_card.UserID = current_user.id
         user_card.CreditCardNum = request.form['CreditCardNum']
         user_card.ExpMonth = request.form['ExpMonth']
         user_card.ExpYear  = request.form['ExpYear']
         user_card.CVS      = request.form['CVS']
         user_card.NameOnCard = request.form['NameOnCard']
         db.session.commit()
         flash('Edited Card successfully','success')
         return redirect(url_for('user_profile'))
    return render_template('edit_user_card.html',user_card=user_card)


@app.route('/user_profile/edit_user_shipping/<int:id>', methods=['GET', 'POST'])
def edit_user_shipping(id):
    user_shipping = UserShipping.query.filter_by(id=id).first()
    if request.method == 'POST':
         user_shipping.ShippingAddr = request.form['ShippingAddr']
         user_shipping.ShippingCity = request.form['ShippingCity']
         user_shipping.ShippingState = request.form['ShippingState']
         user_shipping.ShippingZip   = request.form['ShippingZip']

         db.session.commit()
         flash('Successfully updated','success')
         return redirect(url_for('user_profile'))

    return render_template('edit_user_shipping.html',user_shipping=user_shipping)

@app.route('/user_profile/delete_user_card/<int:id>', methods=['GET', 'POST'])
def delete_user_card(id):
    user_card = UserCard.query.filter_by(id=id).first()
    db.session.delete(user_card)
    db.session.commit()
    flash('Successfully deleted','success')
    return redirect(url_for('user_profile'))


@app.route('/user_profile/delete_user_shipping/<int:id>', methods=['GET', 'POST'])
def delete_user_shipping(id):
    print(id)
    user_shipping = UserShipping.query.filter_by(id=id).first()
    print(user_shipping)
    db.session.delete(user_shipping)
    db.session.commit()
    flash('Successfully deleted','success')
    return redirect(url_for('user_profile'))


def validBookObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject
            and "rating" in bookObject and "comments" in bookObject):
        return True
    else:
        return False


# Gets list of books (Might be replaced with books)
@app.route('/list_of_books')
def get_books():
    return jsonify({'books': books})


# Adds books (Might use/replace method at bottom)
@app.route('/list_of_books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if (validBookObject(request_data)):
        new_book = {
            "name": request_data['name'],
            "price": request_data['price'],
            "isbn": request_data['isbn'],
            "rating": request_data['rating'],
            "comments": request_data['comments']
        }
        books.insert(0, new_book)
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/list_of_books/" + str(new_book['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data passed in similar must be similar to this {'name': 'bookname', 'price': 7.99, "
                          "'isbn': 10, 'rating': 2, 'comments': 'comments'}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response


# Gets book details by isbn
@app.route('/book_details/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                'name': book["name"],
                'price': book["price"],
                'rating': book["rating"],
                'comments': book["comments"]
            }
    return jsonify(return_value)


def valid_put_request_data(request_data):
    if "name" in request_data and "price" in request_data and "rating" in request_data and "comments" in request_data:
        return True
    else:
        return False

@app.route('/list_of_books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    if (not valid_put_request_data(request_data)):
        invalidBookObjectErrorMsg = {
            "error": "Valid book object must be passed in the request",
            "helpString": "Data passed in similar must be similar to this {'name': 'bookname', 'price': 7.99, "
                          "'rating': 2, 'comments': 'comments'}"

        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response
    new_book = {
        'name': request_data["name"],
        'price': request_data["price"],
        'rating': request_data["rating"],
        'comments': request_data["comments"],
        'isbn': isbn
    }
    i = 0;
    for book in books:
        currentIsbn = book["isbn"]
        if currentIsbn == isbn:
            books[i] = new_book
        i += 1
    response = Response("", status=204)
    return response


@app.route('/list_of_books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    updated_book = {}
    if ("name" in request_data):
        updated_book["name"] = request_data['name']
    if ("price" in request_data):
        updated_book["price"] = request_data['price']
    if ("rating" in request_data):
        updated_book["rating"] = request_data['rating']
    if ("comments" in request_data):
        updated_book["comments"] = request_data['comments']
    for book in books:
        if book["isbn"] == isbn:
            book.update(updated_book)
    response = Response("", status=204)
    response.headers['Location'] = "/books/" + str(isbn)
    return response


@app.route('/list_of_books/<int:isbn>', methods=['DELETE'])
def delete_a_book(isbn):
    i = 0;
    for book in books:
        if book["isbn"] == isbn:
            books.pop(i)
            response = Response("", status=204)
            return response
        i += 1
    invalidBookObjectErrorMsg = {
        "error": "Book with the isbn number that was provided was not found, unable to delete"
    }
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=404, mimetype='application/json')
    return response;


# book edit view
@app.route('/book/<int:id>')
def book(id):
    book = Book.query.filter_by(id=id).first()
    author = Authors.query.filter_by(AuthorName=book.authorName).first()
    return render_template('book.html', book=book, author=author)


@app.route('/user_books/<int:id>')
def user_book(id):
    # check book with the id that belongs to the user
    books = Book.query.filter_by()
    return render_template('user_books.html')


@app.route('/add_to_cart/<int:book_id>')
def add_to_cart(book_id):
    user_id = current_user.id
    # check thru books for the book with the specified id 
    # check thru the book copy for the book copy with the id
    book = Cart(user_id=user_id, book_id=book_id, quantity=1)
    db.session.add(book)
    db.session.commit()

    flash('Book added to cart', 'success')
    return redirect(url_for('index'))


@app.route('/save_for_later/<int:book_id>')
def save_for_later(book_id):
    user_id = current_user.id
    # check thru books for the book with the specified id 
    # check thru the book copy for the book copy with the id
    book = Saveforlater(user_id=user_id, book_id=book_id)
    db.session.add(book)
    db.session.commit()

    book_to_delete = Cart.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    print(book_to_delete.id)
    # print(book_to_delete)
    db.session.delete(book_to_delete)
    db.session.commit()

    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    # query the db for the cart object with the 
    # user id of the user of the current session
    user_id = current_user.id
    user_cart = Cart.query.filter_by(user_id=user_id).all()
    all_saved_books = Saveforlater.query.filter_by(user_id=user_id).all()
    user_books = []
    saved_books = []
    saved_books_price = 0
    total_price = 0

    for book in user_cart:
        book_id = book.book_id
        book = Book.query.filter_by(id=book_id).first()
        total_price = book.price + total_price
        user_books.append(book)

    for book in all_saved_books:
        book_id = book.book_id
        book = Book.query.filter_by(id=book_id).first()
        saved_books_price = saved_books_price + book.price
        saved_books.append(book)

    cart_books = len(user_books)
    total_saved_books = len(all_saved_books)

    return render_template('cart.html', total_price=total_price, books=user_books, saved_books=saved_books,
                           saved_books_price=saved_books_price, cart_books=cart_books,
                           total_saved_books=total_saved_books)


@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    book_to_delete = Cart.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    db.session.delete(book_to_delete)
    db.session.commit()

    return redirect(url_for('cart'))


@app.route('/delete_saved_book/<int:book_id>')
def delete_saved_book(book_id):
    book_to_delete = Saveforlater.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    db.session.delete(book_to_delete)
    db.session.commit()

    return redirect(url_for('cart'))


@app.route('/move_to_cart/<int:book_id>')
def move_to_cart(book_id):
    user_id = current_user.id
    # check thru books for the book with the specified id 
    # check thru the book copy for the book copy with the id
    book = Cart(user_id=user_id, book_id=book_id, quantity=1)
    db.session.add(book)
    db.session.commit()

    book_to_delete = Saveforlater.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    db.session.delete(book_to_delete)
    db.session.commit()

    return redirect(url_for('cart'))



@app.route('/addbook', methods=['GET', 'POST'])
def addbook():
    if request.method == 'POST':
        book_name = request.form['book_name']
        book_description = request.form['book_description']
        book_price = request.form['book_price']
        book = Book(title=book_name, description=book_description, price=book_price)
        db.session.add(book)
        db.session.commit()

    return render_template('addbook.html')


@app.route('/author', methods=['GET', 'POST'])
def author_page():
    return render_template('author.html')


@app.route('/comments', methods=['GET', 'POST'])
def comments():
    return render_template('comments.html')


@app.route('/rating', methods=['GET', 'POST'])
def star_rating():
    return render_template('star_rating.html')


if __name__ == '__main__':
    app.run(debug=True)
