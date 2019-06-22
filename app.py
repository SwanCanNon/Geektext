from flask import Flask,flash, render_template,redirect,make_response,request,url_for,session  
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators,SubmitField 
from wtforms.validators import InputRequired,Email,Length 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:aa09@localhost/geekText"
db = SQLAlchemy(app)
migrate = Migrate(app,db)

book_copies = db.Table('book_copies',
    db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
    db.Column('book_id',db.Integer,db.ForeignKey('book.id'))
)

class RegistrationForm(Form):
    username = StringField('name',[validators.Length(min=4,max=25)])
    email    = StringField('email',[validators.Length(min=6,max=35)])
    password = PasswordField('password',[
        validators.DataRequired(),
        validators.EqualTo('confirm',message="Passwords must match")
    ])
    confirm  = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS',[validators.DataRequired])
    submit  = SubmitField('Sign up')

class LoginForm(Form):
    name = StringField('name',validators=[InputRequired(),Length(min=8,max=80)])
    password = PasswordField('password',validators=[InputRequired(),Length(min=8,max=60)])
    remmember = BooleanField('remmember me')
    submit   = SubmitField('Login')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    password = db.Column(db.String(128))
    books = db.relationship('Book',secondary=book_copies,backref=db.backref('users',lazy='dynamic'))

class Book(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    image_path = db.Column(db.String(128))
    title = db.Column(db.String(128))
    description = db.Column(db.String(128))
    price = db.Column(db.Float)

class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(128))
    user_id = db.Column(db.Integer,db.ForeignKey('book.id'))

@app.route('/')
def index():
    return render_template('books.html')

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    # session.pop('user',None)

    if 'user' in session:
        return redirect(url_for(index))

    if request.method == 'POST':
        
        username = request.form['name']
        password = request.form['password']
        exists = db.session.query(User.id).filter_by(name=username,password=password).scalar() is not None

        if exists == True: 
            # username and password found now they will be logged in 
            session['user'] = request.form['name'] 
            flash("You are now logged in",'success')
            return redirect(url_for('books'))
        else:          
            flash("That username could not be found/password/username are incorrect",'error')
            return redirect(url_for("login"))
    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    session.pop('user',None)
    flash("You have been logged out",'success')
    return render_template('books.html')

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

@app.route('/books')
def books():
    books = Book.query.all()
    print(books)

    for book in books:
        print(book.title)
        print(book.description)
        print(book.price)

    return render_template('books.html',books=books)

@app.route('/addbook',methods=['GET','POST'])
def addbook():
    if request.method == 'POST':
        book_name = request.form['book_name']
        book_description = request.form['book_description']
        book_price = request.form['book_price']

    return render_template('addbook.html')

# book edit view 
@app.route('/book/<int:id>')
def book(id):
    book = Book.query.filter_by(id=id).first()

    return render_template('book.html',book=book)

@app.route('/user_books')
def user_books(id):
    # check all books with the ide of the specified user
    return render_template('user_books.html')

@app.route("/search",methods=["POST"])
def search():
    print(request.form['search'])
    query = request.form['search']

    # search thru all the books and find a book with the matching 
    # book name and return it in the results 

    return render_template("search_results.html",query=query)

@app.route('/user_books/<int:id>')
def user_book(id):
    # check book with the id that belongs to the user
    books = Book.query.filter_by()
    return render_template('user_books.html')

@app.route('/add_to_cart<int:id>')
def add_to_cart(id):
    # check thru books for the book with the specified id 
    # check thru the book copy for the book copy with the id 
   
    return render_template('books.html')

@app.route('/cart')
def cart():
    # query the db for the cart object with the 
    # user id of the user of the current session

    return render_template('cart.html')

@app.route('/checkout',methods=['GET','POST'])
def checkout():
    if request.method == 'GET':
        print("het")
    else:
        pass 
    # query the db for the cart object 
    # make a new transaction class 
    # add transaction to the database 

    return render_template('checkout.html')

@app.route('/success_checkout')
def success_checkout():
    # have a flash message sent to the user that the operation 
    # was successful and a display of their transaction 
    # maybe add a pdf 

    return render_template('success_checkout')


if __name__ == '__main__':
    app.run(debug=True)

