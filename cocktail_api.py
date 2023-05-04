from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from db_manager import db_session
from cocktail_classes import Cocktail, Ingredient
from flask_bootstrap import Bootstrap
from flaskext.markdown import Markdown
import random 

app = Flask(__name__)
Bootstrap(app)
Markdown(app)

cts = None

def check_globals():
    global cts 

    if not cts:
        cts = Cocktail.query.all()

@app.route('/')
def home():
    check_globals()
    return render_template("home.html")

@app.route('/cocktails/')
def cocktails():
    check_globals()
    return render_template("search.html")

@app.route('/search/')
def search():
    check_globals()
    user_input = request.args.get('search')
    matched = False
    for c in cts:
        if c.name.lower() == user_input.lower():
            ingr_list = c.display()
            cocktail = c
            matched = True
            return render_template("cocktails.html", drink=cocktail, ingrs=ingr_list)
    if matched == False:
        if user_input.lower() == "random":
            random_drink = random.randint(0, 424) # found that there was 425 cocktails in the scraper file 
            cocktail = cts[random_drink]
            ingr_list = cocktail.display()
            return render_template("cocktails.html", drink=cocktail, ingrs=ingr_list)
        else:
            return render_template("home.html")
    
@app.route('/ingredients/<string:name>/')
def ingredients(name):
    ingrs = Ingredient.query.all()
    for i in ingrs:
        if i.name.lower() == name.lower():
            ingredient = i
    return render_template("ingredients.html", ingredient=ingredient)


if __name__ == '__main__':
    # run your app
    app.run(host='0.0.0.0', port='9099')
    