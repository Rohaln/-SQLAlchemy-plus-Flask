from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
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
session = Session()

artist_list = session.query(Poet).all()
artist_choices = []
for item in artist_list:
   mylist=[]
   mylist.append(item.id)
   mylist.append("{}, {}".format(item.lastName, item.firstName) )
   my_tuple = tuple(mylist)
   artist_choices.append(my_tuple)
print(artist_choices)
session.commit()

from form20 import Artist_Form, Painting_Form

from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)

app.config["SECRET_KEY"]='I_HATE_SQLIE!'

@app.route("/")
def myredirect():
   return redirect(url_for('artist_form'))

@app.route('/artist_form', methods=['GET', 'POST'])
def artist_form():
   form = Artist_Form()
   if form.validate_on_submit():
      result = request.form
      a_Poet = Poet(lastName= result["lastName"], firstName=result["firstName"], country = result["country"], birthDate=result["birthDate"], deathDate=result["deathDate"], networth=result["networth"])
      session.add(a_Poet)
      session.commit()  

      return render_template('artist_form_handler.html', title="Insert Poet Form Handler", header="Insert Poet Form handler", result=result)
   return render_template('artist_form.html', title="Insert Poet Form", header="Insert Poet Form", form=form)

@app.route('/painting_form', methods=['GET', 'POST'])
def painting_form():
   form = Painting_Form()
   if form.validate_on_submit():
      print("submit valid")
      result = request.form
      
      a_painting = Poems(title= result["title"], filename=result["filename"], poet_id = result["poet_id"])
      session.add(a_painting)
      session.commit() 

      
      return render_template('painting_form_handler.html', title="Insert Painting Form Handler", header="Insert Painting Form handler", result=result)
   else:
      print("either not submit or not valid")
      form.poet_id.choices=artist_choices
   return render_template('painting_form.html', title="Insert Painting Form", header="Insert Painting Form", form=form)

if __name__ == "__main__":
   app.run(debug=True)