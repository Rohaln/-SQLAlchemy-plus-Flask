# WTF using flask wt-forms

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField
from wtforms.validators import InputRequired, Length

class Artist_Form(FlaskForm):
   lastName = StringField("last name", 
   validators=[InputRequired(message="You must enter a last name"), Length(min=2, max=60, message="Last Name length must be between 2 and 60 characters")])
     
   firstName = StringField("first name", 
   validators=[InputRequired(message="You must enter a first name"), Length(min=2, max=60, message="First Name length must be between 2 and 60 characters")])
   
   country = StringField("Country", 
   validators=[InputRequired(message="You must enter a country"), Length(min=2, max=60, message="Country length must be between 2 and 60 characters")])

   birthDate = StringField("Birth Date")

   deathDate = StringField("Death Date")

   networth = StringField("Net Worth")
     
   submit = SubmitField("Insert Poet")

class Painting_Form(FlaskForm):

   title = StringField("Title", 
   validators=[InputRequired(message="You must enter a title"), Length(min=2, max=60, message="Title length must be between 2 and 60 characters")], 
   default="Untitled")
     
   #painter_id = SelectField("Painter ID ", choices=[("1","Manet, Edouard"), ("2","Seurat, Georges")])
   poet_id = SelectField("Painter ID ")
   #painter_id = QuerySelectField("Painter ID ", query_factory=)

   releasedate = StringField("Release Date")    
   
   submit = SubmitField("Insert Poem")