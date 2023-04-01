from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet
from werkzeug.utils import secure_filename
from datetime import datetime;
import os

app = Flask(__name__)
#key 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = 'qwertyuixcvbnm'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/two_database'
app.config['UPLOAD_FOLDER'] = "C:\\Users\\suraj\\OneDrive\Documents\\Development\project\\blog_post\static\\img"

image = os.path.join('/static/','img')

key =  Fernet.generate_key()
fernet = Fernet(key) 

db = SQLAlchemy(app)

class Users(db.Model):
    email = db.Column(db.String(25), primary_key = True, nullable=False)
    user_id = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    rePassword = db.Column(db.String(50), nullable=False)
    phoneNo =db.Column(db.Integer, nullable=False)


class Blogs(db.Model):
    s_no = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(20), nullable = False)
    img1 = db.Column(db.String(30), nullable = False)
    img2 = db.Column(db.String(30), nullable = False)
    img1sub =db.Column(db.String(50), nullable = False)
    img2sub=  db.Column(db.String(50), nullable = False)
    author_name = db.Column(db.String(30), nullable = False)
    date_time = db.Column(db.DateTime, nullable = False)
    content = db.Column(db.String(300), nullable = False)
    Blog_type = db.Column(db.String(30), nullable =False)


@app.route('/')
def index():
    if('username' not in session ):
        blog_items = Blogs.query.all()
        return render_template('index.html', blog_items = blog_items, session = session, user = 'username', image=image)
    return redirect(url_for('home', email = session['username']))


@app.route('/home/<email>')
def home(email):
    # print(email)
    if (session['username'] == email):
        # print(fernet.encrypt(email.encode()))
        blog_items = Blogs.query.all()
        return render_template('index.html', blog_items = blog_items, email = email , user = 'username' ,session = session, image=image)
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signuping', methods=['GET', 'POST'])
def signIn():
    # if session['username'] != None:
    if(request.method == 'POST'):
        email = request.form.get('email')
        userid = request.form.get('userid')
        password = request.form.get('password')
        repassword = request.form.get('re_password')
        phoneno = request.form.get('phoneno')
        entry = Users(email = email, user_id = userid, password = password , rePassword = repassword, phoneNo = phoneno)
        db.session.add(entry)
        db.session.commit()
        session['username'] = email
        return redirect(url_for('home', email = email))


@app.route('/login_auth', methods=['GET', 'POST'])
def login_auth():
    if request.method == 'POST':
        email  = request.form.get('email')
        password  = request.form.get('password')
        # print("email from html form "+email)
        check = Users.query.filter_by(email = email).first()
        if(check is None):
            flash("Invalid input")
        else:
            if(check.password == password):
                session['username'] = email
                # print(session['username'])
                return redirect(url_for('home', email = email, user = 'username', session = session['username']))
    return redirect(url_for('login'))

@app.route('/log_out')
def logOut():
    session.pop('username' , None)
    return redirect(url_for('login'))

@app.route('/signup')
def sign():
    return render_template('signup.html')


@app.route('/blog-content/', methods=['GET','POST'])
def blog_content():
    if('username' in session):
        ContentData  =  Blogs.query.filter_by( title = request.args.get('title')).all();
        return render_template('blogContent.html', email = session['username'] ,user = 'username', session = session, contentData = ContentData, image = image)
    else:
        return redirect(url_for('login'))

@app.route('/create-blog/')
def handelCreateBlogAtLogout():
    return redirect(url_for('login'))

@app.route('/submitBlog' , methods = ['GET', 'POST'])
def submittingBlog():
    if 'username' in session:
        if request.method == 'POST':
            title = request.form.get('title')
            anytorname = request.form.get('authorName')
            typ = request.form.get('contentType')
            dateAndTime = request.form.get('dateAndTime')
            print(dateAndTime)
            content = request.form.get('Content')
            img1head = request.form.get('imgSubhead1')
            img1head2 = request.form.get('imgSubhead2')
            fl = request.files['file1']
            fl2 = request.files['file2']
            date__time = datetime.now();
            enrty = Blogs(title = title, img1 = fl.filename, img2 = fl2.filename, author_name = anytorname, date_time = date__time, content = content, Blog_type = typ, img1sub = img1head, img2sub = img1head2)
            fl.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(fl.filename)))
            fl2.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(fl2.filename)))
            db.session.add(enrty)
            db.session.commit()
            flash('Submit Successfull')
            flash("SuccessFull Uploaderd")
        return redirect(url_for("create_blog", email = session['username']))
    return redirect(url_for('login'))


@app.route('/create-blog/<email>')
def create_blog(email):
    if('username' in session):
        return render_template("blogForm.html", email = email, user= 'username', session = session)
    return redirect(url_for('login'))

if __name__=="__main__":
    app.run(debug=True)

