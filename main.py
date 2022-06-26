import json
from bs4 import BeautifulSoup
import pprint
import requests
import pytesseract
import os
from googletrans import Translator
from PIL import Image

file = ""

dictionary_data = {}


def getType(word):
    dicWeb = 'https://www.definify.com/word/'
    html_text = requests.get(dicWeb + word).text
    soup = BeautifulSoup(html_text, 'lxml')

    if 'Verb' in html_text:
        dictionary_data[word]['Type'] = 'Verb'
    elif 'Noun' in html_text:
        dictionary_data[word]['Type'] = 'Noun'
    else:
        dictionary_data[word]['Type'] = 'N/a'


def getPlural(word):
    dicWeb = 'https://www.definify.com/word/'
    html_text = requests.get(dicWeb + word).text
    soup = BeautifulSoup(html_text, 'lxml')
    infoblocks = soup.find_all('div', 'tense-section')
    plural = 'n/a'
    for i in range(2):
        if infoblocks[i].find('b'):
            plural = infoblocks[i].find('b').text
    dictionary_data[word]['Plural'] = plural


def getVerbForms(word):
    verbConjigationWeb = 'https://cooljugator.com/ar/'
    html_text = requests.get(verbConjigationWeb + word).text
    conjDic = {}
    soup = BeautifulSoup(html_text, 'lxml')
    pronouns = soup.find_all('div', class_="ui ribbon label blue conjugation-pronoun")
    conjigations = soup.find_all('div', class_="meta-form")
    translations = soup.find_all('div', class_="meta-translation")
    for i in range(13):
        conjDic[pronouns[i].text] = {}
        conjDic[pronouns[i].text][conjigations[i].text] = translations[i].text
    for i in range(13, 26):
        conjDic[pronouns[i - 13].text][conjigations[i].text] = translations[i].text

    dictionary_data[word]['Conjigations'] = conjDic


def printConjigations(word):
    for key in dictionary_data[word]["Conjigations"]:
        print(key + ":")
        for key2 in dictionary_data[word]["Conjigations"][key]:
            print("\t" + key2 + " - " + dictionary_data[word]["Conjigations"][key][key2])


if __name__ == '__main__':

    if not os.path.exists("C:/GitHubRep/Hackathon2022/Hackathon2022---fpm5/dictionary_file.json"):
        file = open("C:/GitHubRep/Hackathon2022/Hackathon2022---fpm5/dictionary_file.json", "w")
        file.write("{}")

    else:
        file = open("C:/GitHubRep/Hackathon2022/Hackathon2022---fpm5/dictionary_file.json", "r")
        dictionary_data = json.load(file)
    file.close()

    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

    im = Image.open(r'image.png')
    text = pytesseract.image_to_string(im, lang='ara')
    newtext = text.rstrip()
    print(newtext)
    if newtext in dictionary_data:
        print(dictionary_data[newtext]["Translation"])
        print(dictionary_data[newtext]['Type'])
        if dictionary_data[newtext]['Type'] == "Verb":
            printConjigations(newtext)
        elif dictionary_data[newtext]['Type'] == "Noun":
            print(dictionary_data[newtext]["Plural"])
    else:
        translator = Translator()
        dictionary_data[newtext] = {}
        dictionary_data[newtext]["Translation"] = translator.translate(newtext,
                                                                       dest='en').text  # get translation from google
        print(dictionary_data[newtext]["Translation"])
        getType(newtext)

        print(dictionary_data[newtext]['Type'])
        if dictionary_data[newtext]['Type'] == "Verb":
            getVerbForms(newtext)
            printConjigations(newtext)
        elif dictionary_data[newtext]['Type'] == "Noun":
            getPlural(newtext)
            print(dictionary_data[newtext]["Plural"])

        file = open("C:/GitHubRep/Hackathon2022/Hackathon2022---fpm5/dictionary_file.json", "w")
        file.write(json.dumps(dictionary_data))
        file.close()
