import os
import re
import csv
import requests
from tqdm import tqdm
from datetime import date
from bs4 import BeautifulSoup

URL = "https://www.bbcgoodfood.com/recipes/chicken-noodle-soup"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) '
                         'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 '
                         'Safari/605.1.15'}

props2scrape = ['ratingValue', 'ratingCount', 'cookTime', 'prepTime',
                'totalTime', 'cookingMethod', 'recipeCuisine',
                'recipeCategory', 'keywords']


def scrape_recipe_bbcgoodfood(url_in):
    """
    scrape_recipe_bbcgoodfood scrapes a single recipe web page from
    bbcgoodfood.com
        :input: url_in - url to the recipe webpage
        :output: attributes and text from the recipe
    """

    r = requests.get(url_in, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    # recipe header
    container_header = soup.select('div.recipe-header__details')[0]

    # meta attributes from the header
    meta = container_header.select('meta')
    recipe_attributes = [{meta_i['itemprop']: meta_i['content']}
                         for meta_i in meta if meta_i['itemprop'] in props2scrape]

    # adding difficulty and servings from the header
    for item in container_header.select('span.recipe-details__text'):
        recipe_attributes.append({'details': item.text})

    # recipe ingredients-list
    soup_ingredients = soup.select('div.ingredients-list '
                                   'li.ingredients-list__item')
    recipe_ingredients = [ingredient.text.replace(u'\xa0', u' ') for ingredient in soup_ingredients]

    # recipe method
    soup_method = soup.select('div.method li.method__item')
    recipe_method = [step.text.replace(u'\xa0', u' ') for step in soup_method]

    return {'attributes': recipe_attributes, 'ingredients': recipe_ingredients, 'method': recipe_method}


# def main():
#     url = 'https://www.bbcgoodfood.com/recipes/tomato-soup'
#     recipe_content = scrape_recipe_bbcgoodfood(url)
#     print(recipe_content['attributes'])
#     print(recipe_content['ingredients'])
#     print(recipe_content['method'])
#
#
# if __name__ == '__main__':
#     main()
