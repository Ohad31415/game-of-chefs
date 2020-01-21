"""
Author:  Eli Buhris
"""

MISSING_VALUE = None
URL = r"https://www.bbcgoodfood.com/recipes"

import random
import requests
import re
from bs4 import BeautifulSoup
import time
import json
import os
import sys
import argparse
import pandas as pd
import numpy as np


def get_user_agent():
    """This function picks one user agent from a user agent's list"""
    # User agent chrome
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    ]
    return {'user-agent': random.choice(user_agent_list)}


def url_request(url):
    """This function get URL and tries to send request to it"""
    while True:
        page = requests.get(url, headers=get_user_agent())
        if page:
            if not (page.status_code == 200):
                print("Something wrong  with the request")
                continue
        return page


def get_categories(url_recipes):
    """
    This function get the "URL" (global var) and returns the categories and the urls
    """
    all_categories = {}
    prefix = "https://www.bbcgoodfood.com"
    page = url_request(url_recipes)
    soup = BeautifulSoup(page.text, 'html.parser')
    categories = soup.select("div.section-box__content")[0]
    categories = categories.select("a")
    for category in categories:
        temp_url = category["href"]
        all_categories[category.text] = prefix + temp_url
    return all_categories


def get_sub_categories(category_url):
    """
    This function get url of category and returns the sub-categories and the urls
    """
    sub_categories = {}
    prefix = "https://www.bbcgoodfood.com"
    page = url_request(category_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    categories = soup.select(".category-item > h3 > a")
    for category in categories:
        temp_url = category["href"]
        sub_categories[category.text] = prefix + temp_url
    return sub_categories

    # categories = categories.select("a")
    # for category in categories:
    #     temp_url = category["href"]
    #     all_categories[category.text] = prefix + temp_url
    # return all_categories


def get_recipes(sub_category_url):
    """
    This function get url of sub - category and returns the urls of the recipes in it
    if available
    """
    try:
        recipes = {}
        prefix = "https://www.bbcgoodfood.com"
        page = url_request(sub_category_url)
        soup = BeautifulSoup(page.text, 'html.parser')

        recipes_list = soup.select(".view-content")[0]
        for recipe in recipes_list:
            try:
                prefix = "https://www.bbcgoodfood.com"
                temp = recipe.a.attrs["href"]

                text = recipe.text.split()
                name = []
                for word in text:
                    if word.isalpha():
                        name.append(word)
                        continue
                    break
                name = " ".join(name)

                recipes[name] = prefix + temp

            except AttributeError:
                continue
        return recipes
    except:
        print("Something wrong")


def get_all_recipe(category):
    all_categories = get_categories(URL)
    # print(list(all_categories.keys()))
    # category = np.random.choice(list(all_categories.keys()), 1)  # pick randomly category
    # chosen_category = all_categories[category[0]]
    # category = np.random.choice(list(all_categories.keys()), 1)  # pick randomly category
    # print(chosen_category, category)

    chosen_category = all_categories[category]
    sub_categories = get_sub_categories(chosen_category)
    # print(list(sub_categories.keys()))

    # sub_category = np.random.choice(list(sub_categories.keys()), 1)  # pick randomly sub_category
    # chosen_category = sub_categories[sub_category[0]]
    # print(chosen_category, sub_category)

    recipes = []

    try:
        for cat in sub_categories.values():
            recipes += [link for link in get_recipes(cat).values()]
    except:
        print(cat)

    return recipes
        # print(recipes)

    # data_dict = False
    # while not data_dict:


# if __name__ == '__main__':
# r = get_all_recipe('Cakes & baking')
# print(len(r))
