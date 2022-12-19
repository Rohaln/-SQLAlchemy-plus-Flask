from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
#from sqlalchemy import func

engine = create_engine('sqlite:///poem.db')
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
   poems = relationship("Painting") # note relationship added to imports above
   
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

