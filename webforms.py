from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,BooleanField, ValidationError,SelectField
from wtforms.validators import DataRequired,EqualTo,Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField

#create LoginForm

class LoginForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    submit = SubmitField("Submit")



#Create a post form
class PostForm(FlaskForm):
    #category_data = Category.query.all()
    #myChoices = [(ski , ski) for ski in category_data]
    category_name = StringField("Category", validators = [ DataRequired()])
    title = StringField("Title",validators= [DataRequired()])
    #content = StringField("Content",validators= [DataRequired()], widget=TextArea())
    content = CKEditorField('Content', validators=[DataRequired()])
    #category_name = StringField("Category name",validators= [DataRequired()])
    slug = StringField("Slug",validators= [DataRequired()])
    submit = SubmitField("Submit")



#create a form class
class UserForm(FlaskForm):
    name = StringField("Name", validators = [DataRequired()])
    username = StringField("Username", validators = [DataRequired()])
    email = StringField("Email", validators = [DataRequired()])
    password_hash = PasswordField('Password',validators = [DataRequired(),EqualTo('password_hash2',message = 'Passwords Must match')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Submit")


#create a form class
class PasswordForm(FlaskForm):
    email = StringField("What's Your Email?", validators = [DataRequired()])
    password_hash = PasswordField("Whats your password")
    submit = SubmitField("Submit")

class NamerForm(FlaskForm):
    name = StringField("What's Your Name?", validators = [DataRequired()])
    submit = SubmitField("Submit")



class CategoryForm(FlaskForm):
    category_name = StringField("Post Category?", validators = [DataRequired()])
    submit = SubmitField("Submit")

class CommentForm(FlaskForm):
    content = StringField("Comment here!",widget=TextArea())
    submit = SubmitField("Submit")



#Create a Search form
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")


