
from bs4 import BeautifulSoup as bs

import requests

import re

import string

import nltk

# nltk.download('punkt')

from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

# nltk.download('stopwords')

from nltk.corpus import stopwords

stopWords = set(stopwords.words('english'))







def _get_wiki_text(url):

    '''Return list with the text from the url divided by paragraph.'''

    source = requests.get(url).text

    soup = bs(source, 'html.parser').find_all('p')

    return [par.text for par in soup]





def _basic_clean(paragraph):

    '''Basic clean include -

        make all lower case

        remove words with number in them

        remove all not letters symbols.

    '''

    words = paragraph.split(' ')

    clean_text = [word.lower() for word in words]

    clean_text = [re.sub(r'\w*\d\w*', '', word) for word in clean_text]

    clean_text = [re.sub(r'[^a-zA-Z]', '', word) for word in clean_text]

    return ' '.join(clean_text)





def _remove_stop_words(paragraph):

    '''Filter words like 'the', 'is', 'are'.'''

    return ' '.join([word for word in paragraph.split(' ') if word not in stopWords])





def _stemming_the_paragraphs(paragraph):

    '''

        The function remove morphological affixes from words, leaving only the word stem.

        for explantion about the algo see "https://tartarus.org/martin/PorterStemmer/"

    '''

    return ' '.join([stemmer.stem(word) for word in paragraph.split(' ')])





def _limit_size_of_string(l, min=200):

    in_list = sorted(l)

    while(len(in_list[0]) < min and len(in_list) > 1):

        in_list[1] += ' ' + in_list[0]

        in_list.pop(0)

        in_list = sorted(in_list)

    return in_list





def get_clean_data(url, *label):

    '''

     This is the function that calld from this module

     the function accepts url and label and return clean_paragraph object.

    '''

    origin_data = _get_wiki_text(url)

    return clean_paragraph(origin_data, _limit_size_of_string
        ([_stemming_the_paragraphs(_remove_stop_words(_basic_clean(p))) for p in origin_data]) ,label, url)









class clean_paragraph():

    """

        This class returned by get_clean_data function

        the class contain the text returened by _get_wiki_text function

        and the clean data after -

        _basic_clean

        _remove_stop_words

        _stemming_the_paragraphs

        and also the label and the url from get_clean_data function

        also sum funcunality.

    """

    def __init__(self, original_data, clean_data, label, url):

        self.original_data = original_data

        self.clean_data = clean_data

        self.label = label

        self.url = url

        self.list = [original_data, clean_data, label, url]





    def __iter__(self):

        '''Make the class iterable (and the ability to use list(clean_paragraph)).'''

        return iter(self.list)





    def __add__(self, other):

        '''Allow to use + sign to add to objects whith the same label.'''

        if (self.label == other.label):

            return clean_paragraph([*self.original_data, *other.original_data], [*self.clean_data, *other.clean_data], self.label, [self.url, other.url])





    def __getitem__(self, index):

        '''Allow to access the object properties by index.'''

        return self.list[index]