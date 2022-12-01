from flask import Flask, render_template

#create a flask instance
app = Flask(__name__)  #helps python find all files

#Create a route decorator
#urls
@app.route('/')

#def index():
    #return "<h1>hello world</h1>"

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


#Create Customm Error pages

#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"),500