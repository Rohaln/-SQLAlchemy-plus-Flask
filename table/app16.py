from sqlalchemy import create_engine
engine = create_engine('sqlite:///./lab16.db')
#engine = create_engine('sqlite:///')

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, Float  

class Songs(Base):
   __tablename__ = 'songs'
   
   id = Column(Integer, primary_key=True)
   artist = Column(String)
   length = Column(Integer)
   title = Column(String)

Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()



import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open("static/data/NewWave.txt", "r") as f:
   for line in f:
      i=0
      if line.strip(): #ignoring blank lines 
         x = line.rstrip().split("|")
         parts = x[1].split(":", 1)#spilt the time at the :
         partOne=int(parts[0])#cast each part to 
         partTwo=int(parts[1])
         sec= (partOne*60)+partTwo#boring math part
         songs = Songs(artist=x[0], length=sec, title=x[2])
         session.add(songs)
session.commit()

query = session.query(Songs)
results = query.all()
for item in results:
   print ("id = {} Artist = {} Length = {} Title = {}".format(item.id, item.artist, item.length, item.title )) 