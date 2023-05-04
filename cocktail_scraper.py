import requests
import csv
import os
from string import ascii_lowercase as alc

# iterate through each letter in the alphabet to get all of the cocktails
for i in alc:
    url = 'https://www.thecocktaildb.com/api/json/v1/1/search.php?f=' + i
    headers = {'user-agent': 'reddit-{}'.format(os.environ.get('USER', 'cse-30332-sp23'))}
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status() # check if the response was successful
        data = r.json()
        rows = []
        if data is not None:
            for item in data['drinks']:
                ingr = str()
                num_ingr = 1
                while(num_ingr < 16 and item[f'strIngredient{num_ingr}'] is not None):
                    #ingr.append(item[f'strIngredient{num_ingr}'])
                    if num_ingr > 1:
                        ingr += ","
                    ingr += item[f'strIngredient{num_ingr}'] 
                    num_ingr += 1
                row = [item['strDrink'], item['strInstructions'], item['strAlcoholic'], item['strGlass'], ingr, item['strDrinkThumb']]
                rows.append(row) 
        # Write the data to a CSV file
        with open('cocktail_info.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerows(rows)
    except:
        print("error")

