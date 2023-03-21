from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/two_database'

db = SQLAlchemy(app)

class Users(db.Model):
    email = db.Column(db.String(25), unique = True, nullable=False)
    user_id = db.Column(db.String(20), primary_key = True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    rePassword = db.Column(db.String(50), nullable=False)
    phoneNo =db.Column(db.Integer, nullable=False)


class Blogs(db.Model):
    s_no = db.Column(db.Integer, nullable = False, primary_key = True)
    title = db.Column(db.String(20), nullable = False)
    img1 = db.Column(db.String(30), nullable = False)
    img2 = db.Column(db.String(30), nullable = False)
    img1sub =db.Column(db.String(50), nullable = False)
    img2sub=  db.Column(db.String(50), nullable = False)
    author_name = db.Column(db.String(30), nullable = False)
    date_time = db.Column(db.DateTime, nullable = False)
    content = db.Column(db.String(300), nullable = False)


@app.route('/')
def index():
    blog_items = Blogs.query.all()
    return render_template('index.html', blog_items = blog_items)

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login_auth', methods=['GET', 'POST'])
def login_auth():
    if request.method == 'POST':
        email  = request.form.get('email')
        password  = request.form.get('password')
        # print("email from html form "+email)
        check = Users.query.filter_by(email = email).first()
        if(check is None):
            return "Invalid input"
        else:
            if(check.password == password):
                return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/signup')
def sign():
    return render_template('signup.html')


@app.route('/blog-content')
def blog_content():
    
    return render_template('blogContent.html')

@app.route('/create-blog')
def create_blog():
    return render_template("blogForm.html")

if __name__ == "__main__":
    app.run()


app.run(debug=True)
