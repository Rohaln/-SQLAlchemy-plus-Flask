from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import relationship
#from sqlalchemy import func

engine = create_engine('sqlite:///poem.db?check_same_thread=False')
#engine = create_engine('sqlite:///')
Base = declarative_base()

class Poet(Base):
   __tablename__ = 'poet'
   
   id = Column(Integer, primary_key=True)
   lastName = Column(String)
   firstName = Column(String)
   country = Column(String)
   birthDate = Column(String)  # I've seen such old dates cause issues so I will stick to strings for now
   deathDate = Column(String)
   networth = Column(String)
   poems = relationship("Poems") # note relationship added to imports above
   
class Poems(Base):
   __tablename__ = 'poems'
   
   id = Column(Integer, primary_key=True)
   title = Column(String)
   releasedate = Column(String)
   poet_id = Column(Integer, ForeignKey('poet.id'))
   # note: ForeignKey added to imports above
   # the argument of ForeignKey is a table.column  
   # note it's table name not class name

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
#Session = scoped_session(sessionmaker(bind=engine))
session = Session()

artist_list = session.query(Poet).all()
artist_choices = []
for item in artist_list:
   mylist=[]
   mylist.append(str(item.id))
   mylist.append("{}, {}".format(item.lastName, item.firstName) )
   my_tuple = tuple(mylist)
   artist_choices.append(my_tuple)
print(artist_choices)
session.commit()

from form20 import Artist_Form, Painting_Form
# note addition of request and redirect to list below
from flask import Flask, render_template, url_for, request, redirect
# WE ARE USING SQLAlchemy's session 
# TOOK OUT FLASK SESSION (for now) SO NOT CONFUSED
app = Flask(__name__)

app.config["SECRET_KEY"]='I_HATE_SQLIE!'

@app.route("/")
def myredirct():
   return redirect(url_for('painting_form'))

@app.route('/painting_form', methods=['GET', 'POST'])
def painting_form():
   form = Painting_Form(from_other=artist_choices)
   form.poet_id.choices=artist_choices
   if form.is_submitted():
      result = request.form
      
      a_painting = Poems(title= result["title"], releasedate=result["releasedate"] )
      a_painting.poet_id = result["poet_id"]
      session.add(a_painting)
      session.commit() 
   
      return render_template('painting_form_handler.html', title="Insert Poem Form Handler", header="Insert Poem Form handler", result=result)

   return render_template('painting_form.html', title="Insert Poem Form", header="Insert Poem Form", form=form)

if __name__ == "__main__":
   app.run(debug=True)