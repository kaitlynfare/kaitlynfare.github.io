import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

#create an engine for your DB using sqlite and storing it in a file named cocktail.sqlite
engine = create_engine('sqlite:///cocktail.sqlite')

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db(): 

    # import your classes that represent tables in the DB and then create_all of the tables
    from cocktail_classes import Cocktail, Ingredient
    Base.metadata.create_all(bind=engine) 

    # read in the cocktail lists from the given CSV 
    with open('cocktail_info.csv', 'r') as csvfile:
        csvreader=csv.reader(csvfile, delimiter=',')
        count = 0
        for row in csvreader: 
            db_session.add(Cocktail(row[0], row[1], row[2], row[3], row[4], row[5]))
            count += 1
        print(count) # count is 425, printed to find number to use later for displaying random cocktails 
        
    # save the database
    db_session.commit()
