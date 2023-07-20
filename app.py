from flask import Flask, render_template,flash,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from webforms import LoginForm, PostForm, PasswordForm, NamerForm, UserForm, CategoryForm, CommentForm, SearchForm
from flask_ckeditor import CKEditor

#create a flask instance
app = Flask(__name__)  #helps python find all files
#add ckeditor
ckeditor = CKEditor(app)
#Add Database
#old SQLITE DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

#New 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/our_users'
#Secret Key
app.config['SECRET_KEY'] = "my super secret key that no one will know"

#Initialize the Database
db = SQLAlchemy(app)
migrate = Migrate(app,db)


#Flask_login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))





@app.route('/user/add', methods = ['GET','POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user is None:
            hashed_pw = generate_password_hash(form.password_hash.data,"sha256")
            user = Users(username = form.username.data,name=form.name.data, email=form.email.data,password_hash = hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.password_hash.data = ''
        flash("User Added Successfully!")

    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form = form, name = name, our_users = our_users)




@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully")

        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html", form = form, name = name, our_users = our_users)

    except:
        flash("Whoops!! there was a problem!")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html", form = form, name = name, our_users = our_users)





#Update DATABASE RECORD
@app.route('/update/<int:id>',methods=['GET','POST'])
@login_required
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method=='POST':
        name_to_update.name = request.form["name"]
        name_to_update.email = request.form["email"]
        name_to_update.username = request.form["username"]
        try:
            db.session.commit()
            flash("User Updated Successfully")
            return render_template("update.html",
            form = form,
            name_to_update = name_to_update)

        except:
            flash("Error!Looks like there was a problem")
            return render_template("update.html",
            form = form,
            name_to_update = name_to_update)
    else:
        return render_template("update.html",
            form = form,
            name_to_update = name_to_update,
            id = id)


@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@app.route('/admin')
@login_required
def admin():
    id = current_user.id
    if id == 13:
        return render_template("admin.html")
    else:
        flash("Sorry! You should be the Admin to access")
        return redirect(url_for('dashboard'))

@app.route('/search', methods = ["POST"])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        #get data from submitted form
        post.searched = form.searched.data
        #Query the Database
        posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
        posts = posts.order_by(Posts.title).all()

        return render_template("search.html", form=form,searched = post.searched,posts = posts)


#Create Login Page
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username = form.username.data).first()
        if user:
            #check the hash
            if check_password_hash(user.password_hash,form.password.data):
                login_user(user)
                flash("Login Successful!!")
                return redirect(url_for('dashboard'))

            else:
                flash("Worng Password - Try Again!")


        else:
            flash("That user doesnt exist!!")
    return render_template('login.html', form = form)


#create logout page
@app.route('/logout', methods =[ 'POST', 'GET'])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out!")
    return redirect(url_for('login'))



#Create Dashboard Page
@app.route('/dashboard', methods = ['GET', 'POST'])
@login_required
def dashboard():

    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    if request.method=='POST':
        name_to_update.name = request.form["name"]
        name_to_update.email = request.form["email"]
        name_to_update.username = request.form["username"]
        try:
            db.session.commit()
            flash("User Updated Successfully")
            return render_template("dashboard.html",
            form = form,
            name_to_update = name_to_update)

        except:
            flash("Error!Looks like there was a problem")
            return render_template("dashboard.html",
            form = form,
            name_to_update = name_to_update)
    else:
        return render_template("dashboard.html",
            form = form,
            name_to_update = name_to_update,
            id = id)


    return render_template('dashboard.html')


#Post related fucntions--------

@app.route('/posts/<int:id>', methods = [ 'GET','POST'])
def post(id):
    print("testing")

    post = Posts.query.get_or_404(id)
    form = CommentForm()
    comments = Comment.query.order_by(Comment.date_posted)
    if request.method=='POST':
   
          poster = current_user.id
    
          com = Comment(content = form.content.data, author_id = poster,post_id = post.id)

          form.content.data = ''
          db.session.add(com)
          db.session.commit()
          return render_template('post.html',post = post, com = com, form=form, comments=comments)



    else:
        return render_template('post.html',post=post,form=form,comments=comments)

    

@app.route('/category', methods = ['GET','POST'])
def category():
    form = CategoryForm()
    if form.validate_on_submit():
        cat = Category(Category_name=form.category_name.data)
        form.category_name.data =''

        db.session.add(cat)
        db.session.commit()

        flash("Category added Successfully")

    return render_template("category.html",form=form)

    




@app.route('/posts')
def posts():
    #grab all the post from database
    posts = Posts.query.order_by(Posts.date_posted)

    

    return render_template("posts.html",posts=posts)



@app.route('/add-post',methods = ['GET','POST'])
#@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        cat_data = Category.query.filter_by(Category_name=form.category_name.data).first()
        poster = current_user.id
        post = Posts(title = form.title.data,content = form.content.data,poster_id = poster,slug = form.slug.data,category_id=cat_data.Category_id)
        
        #Clear the form
        form.title.data = ''
        form.content.data = ''
        form.slug.data = ''
        form.category_name.data=''
        
        
        
        #ADD DATA
        db.session.add(post)
        db.session.commit()

        flash("Blog Post Submitted Successfully")
    #redirt to the webpage
    return render_template("add_post.html",form=form)








@app.route('/posts/edit/<int:id>',methods = ['GET','POST'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        

        #Update database
        db.session.add(post)
        db.session.commit()
        flash("Post Has Been Updated!")

        return redirect(url_for('post',id = post.id))

    if current_user.id == post.poster_id:
        cat_data = Category.query.filter_by(Category_id=post.category_id).first()
        form.category_name.data = cat_data.Category_name
        form.title.data = post.title
        #form.author.data = post.author
        form.slug.data = post.slug
        form.content.data = post.content 
        return render_template('edit_post.html',form=form)


    else:
        flash("You Aren't Authorized to Edit this Post")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html",posts=posts)

    




@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id 
    if id == post_to_delete.poster.id:

        try:
           db.session.delete(post_to_delete)
           db.session.commit()

           #Return a message
           flash("Blog Post was deleted!")
           
           #Grab all the posts from the database
           posts = Posts.query.order_by(Posts.date_posted)
           return render_template("posts.html",posts=posts)
    
        except:
           #Return a error message
           flash("Whoops! there was a problem deleting the Post!")
           #grad all the post from database
           posts = Posts.query.order_by(Posts.date_posted)
           return render_template("posts.html",posts=posts)


    else:

        #Return a message
        flash("You Aren't Authorized to Delete that Post")
           
        #Grab all the posts from the database
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html",posts=posts)




    



#Create Customm Error pages

#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"),500



#def index():
    #return "<h1>hello world</h1>"


#Create a route decorator
#urls
@app.route('/')
def index():
    first_name = "John"
    stuff = "This is <strong>Bold</strong>Text"
    return render_template("index.html",
    first_name = first_name,
    stuff = stuff)

#localhost:5000/user/john
@app.route('/user/<name>')

def user(name):
    return render_template("user.html",name=name)




#create password Test page
@app.route('/test_pw', methods = ['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
   
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data

        #clear the form
        form.email.data = ''
        form.password_hash.data = ''

        #lookup user by email
        pw_to_check = Users.query.filter_by(email = email).first()

        #check hash password
        passed = check_password_hash(pw_to_check.password_hash,password)
        #flash("Form Submitted Successfully")
    return render_template("test_pw.html",
     email = email,
     password = password,
     pw_to_check = pw_to_check,
     passed = passed,
    form = form )



#create name page
@app.route('/name', methods = ['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data 
        form.name.data = ''
        flash("Form Submitted Successfully")
    return render_template("name.html",
     name = name,
    form = form )


#THE DATABASE DESIGN

#Create Blog Model
class Posts(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    #author = db.Column(db.String(225))
    date_posted = db.Column(db.DateTime,default = datetime.utcnow)
    slug = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('category.Category_id'))
    #Forign Key To Link Users(refer to primary key)
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    comments = db.relationship('Comment', backref = 'posts')



#Create Users Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable = False)
    email= db.Column(db.String(120), nullable=False,unique = True)
    date_added = db.Column(db.DateTime,default = datetime.utcnow)
    #do some password work
    password_hash = db.Column(db.String(128))


    #User can have many posts
    posts = db.relationship('Posts', backref = 'poster')
    comments = db.relationship('Comment', backref = 'poster')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    #Create a string
    def __repr__(self):
        return '<Name %r>' % self.name



class Category(db.Model):
    Category_id = db.Column(db.Integer,primary_key = True)
    Category_name = db.Column(db.String(100), nullable = False)

    posts = db.relationship('Posts', backref = 'catss')


class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime,default = datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))





    






