from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
#from sqlalchemy import func

#engine = create_engine('sqlite:///./art.db')
engine = create_engine('sqlite:///')
Base = declarative_base()

# note Table added to imports
# note write_table defined before classes that use it
write_table = Table('write_table', Base.metadata,
    Column('topic_id', Integer, ForeignKey('topic.id')),
    Column('song_id', Integer, ForeignKey('quote.id'))
)

class Author(Base):
   __tablename__ = 'author'
   
   id = Column(Integer, primary_key=True)
   first_name = Column(String)
   last_name= Column(String)
   work = relationship("Quote") # note relationship added to imports above
   
class Quote(Base):
   __tablename__ = 'quote'
   
   id = Column(Integer, primary_key=True)
   topic = Column(String)
   author_id = Column(String, ForeignKey('author.id'))
   contains = relationship("Topic", secondary=write_table, viewonly=True)

class Topic(Base):
   __tablename__ = 'topic'
   
   id = Column(Integer, primary_key=True)
   subject = Column(String)
   talks = relationship("Quote", secondary=write_table, viewonly=True)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open("static/data/quotes.txt", "r") as f:
   for line in f:
      i=0
      if line.strip(): #ignoring blank lines 
         x = line.rstrip().split("|")
         quotes = Quote(author_id=x[0], topic=x[1]) 
         session.add(quotes)
session.commit()
session.flush()

with open("static/data/topics.txt", "r") as f:
   for line in f:
      i=0
      if line.strip(): #ignoring blank lines 
         x = line.rstrip().split(",")
         topics = Topic(subject=x[0]) 
         session.add(topics)
session.commit()
session.flush()
#add in author names maunually
blah = Author(first_name="Jacob", last_name="Braude")
session.add(blah)
blah = Author(first_name="Casey", last_name="Stengel")
session.add(blah)
blah = Author(first_name="Alex", last_name="Karras")
session.add(blah)
blah = Author(first_name="Samuel", last_name="Johnson")
session.add(blah)
session.commit()
session.flush()

# sports have many quotes
session.execute(write_table.insert().values([(1, 13), (1, 9), (1, 5), (1, 7), (1, 8)]))
session.commit()
# knowlege has many quotes
session.execute(write_table.insert().values([(6, 2), (6, 3)]))
session.commit()
session.execute(write_table.insert().values([(6, 1), (7, 1)]))
session.commit()

#List the quotes of a given author.
john = session.query(Author).first()
print("{} wrote the following songs:".format(john.first_name))
for song in john.work:
   print(song.topic)
print("")
#List the quotes that fall under one of your subjects. 
su = session.query(Topic).first()
print("These quotes were written about {}".format(su.subject))
for person in su.talks:
   print(person.topic)
print("")

#List the subjects of a given quote. 
subj = session.query(Quote).first()
print("The subject of this quote '{}'".format(subj.topic))
for person in subj.contains:
   print(person.subject)
print("")