from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
#from sqlalchemy import func

engine = create_engine('sqlite:///players.db')
#engine = create_engine('sqlite:///')
Base = declarative_base()

class Player(Base):
   __tablename__ = 'player'
   
   id = Column(Integer, primary_key=True)
   fullname = Column(String)
   weight = Column(String)
   pos = Column(String)
   height = Column(String)  # I've seen such old dates cause issues so I will stick to strings for now
   college = Column(String)
   salary = Column(String)
   team = relationship("Team") # note relationship added to imports above
   
class Team(Base):
   __tablename__ = 'team'
   
   id = Column(Integer, primary_key=True)
   team = Column(String)
   record = Column(String)
   player_id = Column(Integer, ForeignKey('player.id'))
   # note: ForeignKey added to imports above
   # the argument of ForeignKey is a table.column  
   # note it's table name not class name

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# WTF?
# using flask wt-forms
# run command 
# pip install flask-wtf

from form19 import Artist_Form
# note addition of request and redirect to list below
from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)

# YOU NEED A SECRET_KEY
# A secret key that will be used for securely signing the 
# session cookie and can be used for any other security 
# related needs by extensions or your application. It 
# should be a long random string of bytes, although 
# unicode is accepted too.
app.config["SECRET_KEY"]='Ends in 15D 02H 00M'

@app.route("/")
def myredirct():
   return redirect(url_for('artist_form'))

@app.route('/artist_form', methods=['GET', 'POST'])
def artist_form():
   form = Artist_Form()

   #if form.is_submitted():
   #print(form.validate_on_submit())
   if form.validate_on_submit():
      result = request.form
      a_player = Player(fullname = result["fullName"], weight=result["weight"], pos = result["position"], height=result["height"], 
      college=result["college"],salary=result["sal"])
      session.add(a_player)
      session.commit()  

      return render_template('artist_form_handler.html', title="Insert BasketBall Form Handler", header="Insert BasketBall Form handler", result=result)
   return render_template('artist_form.html', title="Insert BasketBall Form", header="Insert BasketBall Form", form=form)

if __name__ == "__main__":
   app.run(debug=True)