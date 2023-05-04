import re
import os
import requests
from db_manager import Base, db_session
from sqlalchemy import Column, Integer, String, Boolean
class Cocktail(Base):
    __tablename__ = 'cocktails'
    id = Column(Integer, primary_key=True)

    # add all of the Columns 
    name = Column(String)
    instr = Column(String)
    is_alc = Column(String)
    glass = Column(String)
    ingr = Column(String)
    image = Column(String)


    def __init__(self, name: str, instr: str, is_alc: str, glass: str, ingr: str, image: str):
        self.name = name
        self.instr = instr
        self.is_alc = is_alc
        self.glass = glass
        self.ingr = ingr 
        self.image = image 

    def display(self):
        # create ingredient objects and a list of them
        ingrs = self.ingr.split(",")
        self.ingr_list = [Ingredient.get_or_create(ing) for ing in ingrs]
        return self.ingr_list
        

class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)

    # add all of the columns
    name = Column(String)
    descr = Column(String)
    alc = Column(String)
    abv = Column(String)

    def __init__(self, name):
        self.name = name

    @classmethod
    def get_or_create(cls, name):
        # Check if an ingredient with the given name exists in the table
        ingrs = Ingredient.query.all()
        ingredient = None
        for i in ingrs:
            if i.name.lower() == name.lower():
                ingredient = i

        # If the ingredient doesn't exist, create a new one and add it to the table
        if not ingredient:
            ingredient = cls(name=name)
            ingredient.scrape()
            db_session.add(ingredient)
            db_session.commit()

        return ingredient
    
    def scrape(self):
        # get ingredient information from api and set ingredient attributes 
        url = "https://www.thecocktaildb.com/api/json/v1/1/search.php?i=" + self.name 
        headers = {'user-agent': 'reddit-{}'.format(os.environ.get('USER', 'cse-30332-sp23'))}
        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status() # check if the response was successful
            data = r.json()
            if data is not None:
                for item in data['ingredients']:
                    self.descr = item['strDescription']
                    self.alc = item['strAlcohol']
                    self.abv = item['strABV']
        except:
            print("error scraping ingredient")
            



    