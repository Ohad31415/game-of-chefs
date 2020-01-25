'''
The file parse all ingredient list from FoodBase_curated.xml file and save as txt / json file
'''
from lxml import etree
import json

root = "FoodBase_curated.xml"

root = etree.parse(root).getroot()
# get all ingredients
ingridients = [text.text for doc in root.findall('document') for ann in doc.findall('annotation') for text in ann.findall('text')]

ingridients = list(set(ingridients))

#save list into json file
with open('ingridients.txt', 'w') as fd:
    json.dump(ingridients, fd)

print(f'Total ingridients downloaded: {len(ingridients)}')
