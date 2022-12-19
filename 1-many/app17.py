from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
#from sqlalchemy import func

#engine = create_engine('sqlite:///./art.db')
engine = create_engine('sqlite:///')
Base = declarative_base()

class Types(Base):
   __tablename__ = 'types'
   
   id = Column(Integer, primary_key=True)
   typePokemon = Column(String)
   weaknessOne = Column(String)
   weaknessTwo = Column(String)
   supereffectiveOne = Column(String)  # I've seen such old dates cause issues so I will stick to strings for now
   supereffectiveTwo = Column(String)
   pokemon = relationship("Pokemon") # note relationship added to imports above
   
class Pokemon(Base):
   __tablename__ = 'Pokemon'
   
   id = Column(Integer, primary_key=True)
   name = Column(String)
   preevolutionOne = Column(String)
   preevolutionTwo = Column(String)
   painter_id = Column(Integer, ForeignKey('types.id'))
   # note: ForeignKey added to imports above
   # the argument of ForeignKey is a table.column  
   # note it's table name not class name

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

import json
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open('static/data/pokemon.json') as f:
   art = json.load(f)

# to have access to the list element and its index 
# you can use enumerate
for i, poke in enumerate(art["types"]):
   # print("{} -- {} {}".format(i, artist["firstName"], artist["lastName"]))
   a_painter = Types(typePokemon=poke["type"], weaknessOne=poke["weaknessOne"], 
   weaknessTwo=poke["weaknessTwo"], supereffectiveOne=poke["supereffectiveOne"], 
   supereffectiveTwo=poke["supereffectiveTwo"]) 
   session.add(a_painter)
   session.flush()  
   # https://stackoverflow.com/questions/17325006/how-to-create-a-foreignkey-reference-with-sqlalchemy
   # flush the session so that the painter is assigned an id    
   
   for j, poke in enumerate(art["types"][i]["pokemon"]):
      # print("\t", chr(97+j), art["painters"][i]["paintings"][j]["title"])
      a_poke = Pokemon(name=poke["name"], preevolutionOne=poke["preevolutionOne"], preevolutionTwo=poke["preevolutionTwo"])
      a_poke.painter_id = a_painter.id
      session.add(a_poke)

session.commit()

query = session.query(Types).filter(Types.id==2)
poke = query.first()
print ("id={}, {} Pokemon are weak against {} and {}. They are strong against {} and {}.".format(poke.id, poke.typePokemon, 
poke.weaknessOne, poke.weaknessTwo, poke.supereffectiveOne, poke.supereffectiveTwo)) 

for work in poke.pokemon:
   print("Pre-Evolution of {} are {} and {}".format(work.name,work.preevolutionOne, work.preevolutionTwo))


# painters from France
strong = session.query(Types).filter(Types.supereffectiveTwo=="Grass").all()
for poke in strong:
   print ("id={} {} is strong against Grass Pokemon".format(poke.id, poke.typePokemon)) 

pokes = session.query(Types).all()
for poke in pokes:
   print("{} has {} works in the database".format(poke.typePokemon, len(poke.pokemon)))