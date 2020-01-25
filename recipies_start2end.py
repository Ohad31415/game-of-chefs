import argparse
from goodfood import search_results
from scraper import get_all_recipe
from recipes_scraping import scrape_recipe_bbcgoodfood
import requests


def parse_args():
    """
    The function gets user's argument of whether to search according to specific Query or Category
    :returns selected category argument (category_option) or selected search query (args.query)
    """
    category_opts = {'c_b': 'Cakes & baking', 'cu': 'Cuisines', 'ev': 'Events', 'hl': 'Healthy', 'ing': 'Ingredients',
                     'oc': 'Occasions', 'q_e': 'Quick & easy', 'die': 'Special diets', 'veg': 'Vegetarian'}
    category_help = 'chose recipe category:' + str(category_opts)
    parser = argparse.ArgumentParser(description='get argument to limit search')
    parser.add_argument('-q', '--query', type=str, help='recipe search word(s)')
    parser.add_argument('-c', '--category', choices=category_opts.keys(), type=str, help=category_help)

    args = parser.parse_args()
    category_option = category_opts.get(args.category)

    if category_option and args.query:
        raise ValueError('Only one argument can be given')

    if not (category_option or args.query):
        raise ValueError('Please enter a search argument')

    return category_option, args.query


def main():
    """
    The function sparse for recipes in GoodFood according to search query or category
    The recipes includes rating, Cuisine, Ingredients, Methods and additional parameters
    The information is stored in a DataBase
    """
    try:
        # receive query or category for web scraping
        category_selection, query_selection = parse_args()

        # if a query was give, search for all corresponding recipe urls
        if query_selection:
            recipe_urls = search_results(query=query_selection)
        # if a category was give, search for all corresponding recipe urls
        elif category_selection:
            recipe_urls = get_all_recipe(category_selection)
        # go over all recipe urls and retrieve information into a DB
        for url in recipe_urls:
            recipe_content = scrape_recipe_bbcgoodfood(url)
            # todo enter to database

    except ValueError as err:
        print(err)

    except requests.exceptions.ConnectionError as err:
        print("Connection error: {}".format(err))


if __name__ == '__main__':
    main()
