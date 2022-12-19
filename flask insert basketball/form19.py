# WTF using flask wt-forms

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField,SelectField
from wtforms.validators import InputRequired, Length

class Artist_Form(FlaskForm):
   fullName = StringField("Name", 
   validators=[InputRequired(message="You must enter a name"), Length(min=2, max=60, message="length must be between 2 and 60 characters")])
     
   college = StringField("College", 
   validators=[InputRequired(message="You must enter a College"), Length(min=2, max=60, message="length must be between 2 and 60 characters")])
   
   height = StringField("Height", 
   validators=[InputRequired(message="You must enter a Height")])

   weight = StringField("Weight")

   sal = StringField("Salary")

   position = SelectField(u'Postion', 
   choices=[('C', 'Center'), ('F', 'Forward'), ('G', 'Guard'),('SF', 'Small Forward'), ('PF', 'Power Forward'), ('PG', 'Point Gaurd'),('SG',' Shooting Guard')],
   validators=[InputRequired(message=" Choose a Position")])
     
   submit = SubmitField("Insert Player")