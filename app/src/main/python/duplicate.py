#!/usr/bin/env python
# coding: utf-8

# In[ ]:



import nltk

nltk.download('punkt')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
import spacy
nlp = spacy.load("en_core_web_sm")

import parsedatetime as pdt
from datetime import datetime

import pandas as pd


# In[2]:


def datetime_exists(text):
    calendar = pdt.Calendar()
    time, code = calendar.parse(text)
    return code != 0


# In[3]:


def assign_task(input_text):
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in nltk.word_tokenize(input_text)]
    tagged_words = nltk.pos_tag(lemmatized_words)

    # condense words
    core_word_tag = {'VB', 'NN', 'TO'}
    simplified = [(tagged_words[i][0], tagged_words[i][1]) for i in range(len(tagged_words)) if tagged_words[i][1] in core_word_tag]
    #print(simplified)

    modules = []
    # check whether input contains datetime info for calendar
    if datetime_exists(input_text):
        modules.append('calendar')
    # word set for each module
    calendar_set = {'schedule'}
    search_set = {'search', 'look', 'seek'}
    shopping_set = {'buy', 'purchase', 'shop', 'get', 'order'}
    # a list of items that cannot be bought but searchable
    unpurchasable_set = {'restaurant', 'dentist', 'clinic', 'hotel', 'grocery','concert'}

    i = 0
    while i < len(simplified):
        if simplified[i][0] == 'find' and simplified[i+1][0] == 'time':
            if 'calendar' not in modules: modules.append('calendar')
        elif simplified[i][0] == 'find' and simplified[i+1][0] in unpurchasable_set:
            if 'search' not in modules: modules.append('search')
        elif simplified[i][0] == 'find' and simplified[i+1][0] not in unpurchasable_set:
            if 'shopping' not in modules: modules.append('shopping')

        if i < len(simplified)-1 and simplified[i][0].lower() in calendar_set and simplified[i+1][1] == 'NN':
            if 'calendar' not in modules: modules.append('calendar')
        if i < len(simplified)-1 and simplified[i][0].lower() in search_set and simplified[i+1][1] == 'NN':
            if 'search' not in modules: modules.append('search')
        elif simplified[i][0].lower() in unpurchasable_set:
            if 'search' not in modules: modules.append('search')
        if i < len(simplified)-1 and simplified[i][0].lower() in shopping_set and simplified[i+1][1] == 'NN':
            if 'shopping' not in modules: modules.append('shopping')
        i += 1

    if len(modules) == 0:
        modules.append('invalid request, please try again')
    # modules = ['hello']
    return modules


# In[4]:


# test_cases = ['find me some time to buy a new iPhone',
#     'find some Korean restaurants to have lunch with John',
#     'have lunch with John',
#     'purchase a new laptop',
#     'do chores',
#     'join a zoom meeting',
#     'Schedule a car wash']

# for test in test_cases:
#     print(test)
#     print(assign_task(test))
#     print()


# In[ ]:





# In[ ]:




