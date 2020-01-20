import argparse
from goodfood import search_results
from scraper import get_all_recipe
from recipes_scraping import scrape_recipe_bbcgoodfood
import requests

def parse_args():
    """the function gets user's argument of whether to search according to specific Key word or Category"""
    category_opts = {'c&b': 'Cakes & baking', 'cu': 'Cuisines', 'ev': 'Events', 'hl': 'Healthy', 'ing': 'Ingredients',
                     'oc': 'Occasions', 'q&e': 'Quick & easy', 'die': 'Special diets', 'veg': 'Vegetarian'}
    category_help = 'chose recipe category:' + str(category_opts)
    parser = argparse.ArgumentParser(description='get argument to limit search: --key_word, --category')
    parser.add_argument('--key_word', type=str, help='recipe search word(s)')
    parser.add_argument('--category', choices=category_opts.keys(), type=str, help=category_help)

    args = parser.parse_args()
    category_option = category_opts.get(args.category)

    if category_option and args.key_word:
        print('Only one argument can be given')
        return None

    if not (category_option and args.key_word):
        print('Please enter a search argument')
        return None

    return category_option, args.key_word


def main():
    # gets user's arguments (if exist)
    category_selection, key_word_selection = parse_args()

    try:
        # if a key_word was give, search for all corresponding recipes
        if key_word_selection:
            recipe_urls = search_results(query=key_word_selection)
        elif category_selection:
            recipie_urls = get_all_recipe(category_selection)

        for url in recipie_urls:
            recipe_content = scrape_recipe_bbcgoodfood(url)
            #todo enter to database

    except requests.exceptions.ConnectionError as err:
        print("Connection error: {}".format(err))


if __name__ == '__main__':
    main()
