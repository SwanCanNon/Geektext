from flask import Flask,flash, render_template,redirect,make_response,request,url_for,session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators,SubmitField 
from wtforms.validators import InputRequired,Email,Length,DataRequired
from flask_login import LoginManager,login_user,UserMixin,logout_user,login_required,current_user
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:YES@localhost/geek_text"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:aa09@localhost/geek_text"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://bce5ce263e3ba7:1543b1ce@us-cdbr-iron-east-02.cleardb.net/heroku_e86cfb095c1e8fa"

db = SQLAlchemy(app)
migrate = Migrate(app,db)

book_copies = db.Table('book_copies',
    db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
    db.Column('book_id',db.Integer,db.ForeignKey('book.id'))
)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RegistrationForm(FlaskForm):
    username = StringField('name',[validators.Length(min=4,max=25)])
    email    = StringField('email',[validators.Length(min=6,max=35)])
    password = PasswordField('password',[
        validators.DataRequired(),
        validators.EqualTo('confirm',message="Passwords must match")
    ])
    confirm  = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS',[validators.DataRequired])
    submit  = SubmitField('Sign up')

class LoginForm(FlaskForm):
    name = StringField('name',validators=[DataRequired(),Length(min=4,max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# password need to have uppercase 
# lowercase 
# special character
# email needs to have the at 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    password = db.Column(db.String(128)) 
    books = db.relationship('Book',secondary=book_copies,backref=db.backref('users',lazy='dynamic'))
    user_cards = db.relationship('UserCard',backref='user')
    user_shippings = db.relationship('UserShipping',backref='user')
    def __str__(self):
        return self.name

class UserCard(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    UserID = db.Column(db.Integer,db.ForeignKey('user.id'))
    CreditCardNum = db.Column(db.Integer)
    ExpMonth = db.Column(db.Integer)
    ExpYear = db.Column(db.Integer)
    CVS = db.Column(db.Integer)
    NameOnCard = db.Column(db.String(128))

class UserShipping(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    UserID = db.Column(db.Integer,db.ForeignKey('user.id'))
    ShippingAddr = db.Column(db.String(128))
    ShippingCity = db.Column(db.String(128))
    ShippingState = db.Column(db.String(128))
    ShippingZip = db.Column(db.String(128))

class Book(db.Model):
    id = db.Column(db.Integer,primary_key=True)
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
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(128))
    user_id = db.Column(db.Integer,db.ForeignKey('book.id'))

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

@app.route('/',methods=['GET','POST'])
def real_index():
    return redirect(url_for('index'))


@app.route('/books',methods=['GET','POST'])
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
    return render_template('books.html',books=books)

@app.route('/login',methods=['GET','POST'])
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
                flash("You are now logged in",'success')
                return redirect(url_for('index'))
            else:
                flash("That username could not be found/password/username are incorrect",'error')

    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out",'success')
    return redirect(url_for('index'))

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if request.method == "POST":
        # access the username, password, email 
        # access the db object and create new user 
        username = request.form['username']
        password = request.form['password']
        email    = request.form['email']
        # check if a user already exists 
        #  with that username 
        exists = db.session.query(User.id).filter_by(name=username).scalar() is not None 

        if exists == True: 
            # session flash that someone already exists with that username
            flash("Someone already exists with that username",'error')
            return redirect(url_for('register'))
        else:  
            # create a new user with that password and username
            # and email 
            new_user = User(name=username,password=password,email=email) 
            # in the homepage show a flask message saying 
            # you are now registered 
            db.session.add(new_user) 
            db.session.commit()            
            # redirect them to the homepage 
            session['user'] = request.form['username']
            flash("You were successfully registered",'success')
            return redirect(url_for("index")) 

    return render_template('register.html',form=form)

@app.route('/user_profile',methods=['GET','POST'])
@login_required
def user_profile():
    print("current user in user profile function " + current_user.name)
    if current_user.is_authenticated:
        current_user_id = current_user.get_id()
        current_user = User.query.filter_by(id=current_user_id).first()
        user_shippings = current_user.user_shippings
        user_cards = current_user.user_cards

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        current_user.name = name 
        current_user.email = email 
        current_user.password = password 
        db.session.commit()
        flash('successfully updated','success')
        return redirect(url_for('user_profile'))

    return render_template('user_profile.html',user_shippings=user_shippings,user_cards=user_cards)

@app.route('/add_user_card',methods=['GET','POST'])
def add_user_card():

    if request.method == 'POST':
        user_id = request.form['UserID']
        credit_card_num = request.form['CreditCardNum']
        expMonth = request.form['ExpMonth']
        expYear  = request.form['ExpYear']
        cvs      = request.form['CVS']
        nameOnCard = request.form['NameOnCard']
        new_card = UserCard(UserID=user_id,CreditCardNum=credit_card_num,ExpMonth=expMonth,ExpYear=expYear,CVS=cvs,NameOnCard=nameOnCard)
        db.add(new_card)
        db.commit()
        flash('new card succesfully added','success')
        return redirect(url_for('user_profile'))

    return render_template('add_user_card.html')


@app.route('/add_user_shipping',methods=['GET','POST'])
def add_user_shipping():
    if request.method == 'POST':
        UserID = request.form['UserID']
        ShippingAddr = request.form['CreditCardNum']
        ShippingCity = request.form['ExpMonth']
        ShippingState = request.form['ExpYear']
        ShippingZip   = request.form['CVS']
        new_user_shipping = UserShipping(UserID=UserID,ShippingAddr=ShippingAddr,ShippingCity=ShippingCity,ShippingState=ShippingState,ShippingZip=ShippingZip)
        db.add(new_user_shipping)
        db.commit()
        flash('new shipping succesfully added','success')
        return redirect(url_for('user_profile'))

    return render_template('add_user_shipping.html')

@app.route('/user_profile/edit_user_card/<int:id>',methods=['GET','POST'])
def edit_user_card(id):
    user_card = UserCard.query.filter_by(id=id)
    if request.method == 'POST':
         user_card.UserID = request.form['UserID']
         user_card.CreditCardNum = request.form['CreditCardNum']
         user_card.ExpMonth = request.form['ExpMonth']
         user_card.ExpYear  = request.form['ExpYear']
         user_card.CVS      = request.form['CVS']
         user_card.NameOnCard = request.form['NameOnCard']
         db.session.commit()
         flash('Edited Card successfully','success')
    return render_template('edit_user_card.html',user_card=user_card)

@app.route('/user_profile/edit_user_shipping/<int:id>',methods=['GET','POST'])
def edit_user_shipping(id):
    user_shipping = UserShipping.query.filter_by(id=id)
    if request.method == 'POST':
         user_shipping.UserID = request.form['UserID']
         user_shipping.ShippingAddr = request.form['CreditCardNum']
         user_shipping.ShippingCity = request.form['ExpMonth']
         user_shipping.ShippingState = request.form['ExpYear']
         user_shipping.ShippingZip   = request.form['CVS']

    return render_template('edit_user_shipping.html',user_shipping=user_shipping)


@app.route('/user_profile/delete_user_card/<int:id>',methods=['GET','POST'])
def delete_user_card(id):
    user_card = UserCard.query.filter_by(id=id)
    db.session.delete(user_card)
    flash('Successfully deleted','success')
    return redirect(url_for('user_profile'))


@app.route('/user_profile/delete_user_shipping/<int:id>',methods=['GET','POST'])
def delete_user_shipping(id):
    user_shipping = UserShipping.query.filter_by(id=id)
    db.session.delete(user_shipping)
    flash('Successfully deleted','success')
    return redirect(url_for('user_profile'))

# book edit view 
@app.route('/book/<int:id>')
def book(id):
    book = Book.query.filter_by(id=id).first()
    author = Authors.query.filter_by(AuthorName=book.authorName)
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
    book = Cart(user_id=user_id,book_id=book_id,quantity=1)
    db.session.add(book)
    db.session.commit()
	
    flash('Book added to cart','success')
    return redirect(url_for('index'))

@app.route('/save_for_later/<int:book_id>')
def save_for_later(book_id):
    user_id = current_user.id
    # check thru books for the book with the specified id 
    # check thru the book copy for the book copy with the id
    book = Saveforlater(user_id=user_id,book_id=book_id)
    db.session.add(book)
    db.session.commit()

    book_to_delete = Cart.query.filter_by(user_id=current_user.id,book_id=book_id).first()
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
    user_cart = Cart.query.filter_by(user_id = user_id).all()
    all_saved_books = Saveforlater.query.filter_by(user_id = user_id).all()
    user_books = []
    saved_books  = []
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

    return render_template('cart.html',total_price=total_price,books=user_books,saved_books=saved_books,saved_books_price=saved_books_price,cart_books=cart_books,total_saved_books=total_saved_books)

@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    book_to_delete = Cart.query.filter_by(user_id=current_user.id,book_id=book_id).first()
    db.session.delete(book_to_delete)
    db.session.commit()

    return redirect(url_for('cart'))

@app.route('/delete_saved_book/<int:book_id>')
def delete_saved_book(book_id):
    book_to_delete = Saveforlater.query.filter_by(user_id=current_user.id,book_id=book_id).first()
    db.session.delete(book_to_delete)
    db.session.commit()

    return redirect(url_for('cart'))

@app.route('/move_to_cart/<int:book_id>')
def move_to_cart(book_id):
    user_id = current_user.id
    # check thru books for the book with the specified id 
    # check thru the book copy for the book copy with the id
    book = Cart(user_id=user_id,book_id=book_id,quantity=1)
    db.session.add(book)
    db.session.commit()
    
    book_to_delete = Saveforlater.query.filter_by(user_id=current_user.id,book_id=book_id).first()
    db.session.delete(book_to_delete)
    db.session.commit()
   
    return redirect(url_for('cart'))

@app.route('/success_checkout')
def success_checkout():
    # have a flash message sent to the user that the operation 
    # was successful and a display of their transaction 
    # maybe add a pdf 

    return render_template('success_checkout')

@app.route('/addbook',methods=['GET','POST'])
def addbook():
    if request.method == 'POST':
        book_name = request.form['book_name']
        book_description = request.form['book_description']
        book_price = request.form['book_price']
        book = Book(title=book_name,description=book_description,price=book_price)
        db.session.add(book)
        db.session.commit()

    return render_template('addbook.html')
	
@app.route('/author', methods=['GET','POST'])
def author_page():
    
    return render_template('author.html')

if __name__ == '__main__':
    app.run(debug=True)

