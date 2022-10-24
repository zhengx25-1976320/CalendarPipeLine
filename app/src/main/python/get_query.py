#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nltk


# In[2]:


def generate_query(tagged_words, i):
    tag_set = {'NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'CD'}
    stop_words = {'to', 'for'}
    query = ''
    while i < len(tagged_words):
        if (tagged_words[i][1] in tag_set or tagged_words[i][1] == 'IN') :
            query += str(tagged_words[i][0]) + ' '
        if i < (len(tagged_words)-1) and str(tagged_words[i+1][0]).lower() in stop_words:
            break
        i += 1
    return query.strip()


# In[3]:


def query_for_shopping(input_text):
    tokens = nltk.word_tokenize(input_text)
    tagged_words = nltk.pos_tag(tokens)
    shopping_set = {'buy', 'purchase', 'shop', 'get', 'order'}
    i = 0
    while i < len(tagged_words)-1:
        if tagged_words[i][0].lower() == 'find' and tagged_words[i+1][0].lower() == 'me': # find me somthing
            i += 2  
            query = generate_query(tagged_words, i)
        elif tagged_words[i][0].lower() == 'find' and tagged_words[i+1][1] == 'NN': # find somthing
            i += 1  
            query = generate_query(tagged_words, i)
        elif tagged_words[i][0].lower() in shopping_set:  # e.g. buy somthing
            i += 1
            query = generate_query(tagged_words, i)
        i += 1
    return query


# In[6]:





# In[ ]:




