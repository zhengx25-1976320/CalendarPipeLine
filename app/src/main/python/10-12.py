#!/usr/bin/env python
# coding: utf-8

# **Command Format:**
# 
# Schedule [action] [date/time] [person] [location]
# Schedule a dinner at night with John at Marriot Hotel
# 

# # ## **Libraries**
#
# # In[ ]:
#
#
# get_ipython().system('pip install datefinder')
#
#
# # In[2]:
#
#
# get_ipython().system('pip install parsedatetime')
#
#
# # In[ ]:
#
#
# get_ipython().system('pip install Transformers')
#
#
# # In[ ]:
#
#
# get_ipython().system('pip install word2number')
# get_ipython().system('pip install nltk')
# get_ipython().system('pip install pandas')
# get_ipython().system('pip install spacy')


# In[23]:


import datetime
import re
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('names')
nltk.download('maxent_ne_chunker')
nltk.download('words')
from nltk import ne_chunk
from nltk.tree import Tree
from os.path import dirname, join
import spacy
nlp = spacy.load("en_core_web_sm")

import datefinder
from datetime import datetime, timedelta
import parsedatetime as pdt 
import pandas as pd
#from google.colab import drive
from pandas.core.common import random_state
#from transformers import BertTokenizer


# ## **Clean & Tokenization**

# improvemnet needs to be made: make tagged_word as a dict, consider to shorten the text for the last if, one option is to return a noun instead of the whole text

# In[24]:


# tag doc: https://www.guru99.com/pos-tagging-chunking-nltk.html


# In[25]:


# helper functions

# return phrases before words like "to"
def generate_query(tagged_words, i):
    tag_set = {'NN', 'NNS', 'NNP', 'NNPS', 'JJ'}
    stop_words = {'to', 'for'}
    query = ''
    while i < len(tagged_words):
        if (tagged_words[i][1] in tag_set or tagged_words[i][1] == 'IN') :
            query += str(tagged_words[i][0]) + ' '
        if i < (len(tagged_words)-1) and str(tagged_words[i+1][0]).lower() in stop_words:
            break
        i += 1
    return query.strip()

# split text into two parts: treat first part (before 'to') as possible query, and second part as new text
# e.g., 'find me some restaurants to have dinner tomorrow night' ---> 'restaurants' + 'to have dinner tomorrow night'
def get_possible_query(text):
    #doc = nlp(text)
    #tagged_words = [(token, token.tag_) for token in doc]
    tokens = nltk.word_tokenize(text)
    tagged_words = nltk.pos_tag(tokens)
    #print(tagged_words)
    query_signal = {'find', 'search', 'seek', 'look'} # list words for potential query request
    stop_words = {'to', 'for'}
    query = ''
    new_text = ''
    i = 0
    while i < len(tagged_words)-1:
        if (str(tagged_words[i][0]).lower() in query_signal) and (str(tagged_words[i+1][0]).lower() in stop_words):
            i += 2  
            query = generate_query(tagged_words, i)
        elif str(tagged_words[i][0]).lower() in query_signal:
            i += 1
            query = generate_query(tagged_words, i)
        if i < (len(tagged_words)-1) and str(tagged_words[i+1][0]).lower() in stop_words:
            break
        i += 1

    if query == '':
        new_text = text
    else:
        for j in range(i+1, len(tagged_words)):
            new_text += str(tagged_words[j][0]) + ' '
    return query, new_text.strip()


# In[26]:


# TEST CASES
#get_possible_query('find me a restaurant in U district to have a lunch')
#get_possible_query('find a hospital near me for vaccine')
#get_possible_query('look for grocery in downtown to have shopping with Jim')
#get_possible_query('schedule a lunch with john at restaurant next friday')
#get_possible_query('Find some time for me tomorrow to play basketball')
#get_possible_query('Find Korean restaurant in U District for my lunch with John next Tuesday')
# get_possible_query('find me some restaurants to have dinner tomorrow night')


# In[27]:


#Perform event title generator using nltk tokenizer
"""
Possible combinations that have been considered:
- noun + noun
- verb + noun
- noun + IN (with) + noun 
- noun 
"""
from nltk import pos_tag
def get_nn(text):
    query, text = get_possible_query(text)
    tokens = nltk.word_tokenize(text)
    pos = nltk.pos_tag(tokens)

    #doc = nlp(text)
    #tagged_words = [(token, token.tag_) for token in doc]

    # use pos_tag from nltk
    tagged_words = nltk.pos_tag(tokens)
    #print(tagged_words)
    noun_set = {'NN', 'NNS', 'NNP', 'NNPS'} 
    verb_set = {'VB', 'VBd', 'VBG', 'VBN', 'VBP', 'VPZ'}
    avoid_set = {'schedule', 'add', 'minutes', 'minute', 'hour', 'hours'}
    prep_set = {'IN', 'TO'}

    s = '' #VB NN or NN NN

    length = len(tagged_words)
    i = 0
    while i < length-1:
        if str(tagged_words[i][0]).lower() in avoid_set:
            i +=1  
            continue
        
        if i < length-2 and tagged_words[i][1] in noun_set and tagged_words[i+1][1] in noun_set and tagged_words[i+2][1] in noun_set: #noun + noun + noun
            if tagged_words[i][1] == 'DT':
                s = str(tagged_words[i+1][0]) + ' ' + str(tagged_words[i+2][0])
                return s.capitalize()
            else:
                s = str(tagged_words[i][0]) + " " + str(tagged_words[i+1][0]) + ' ' + str(tagged_words[i+2][0])
                return s.capitalize()
        elif tagged_words[i][1] in noun_set and tagged_words[i+1][1] in noun_set: #noun + noun
            if tagged_words[i][1] == 'DT':
                s = str(tagged_words[i+1][0])
                return s.capitalize()
            else:
                s = str(tagged_words[i][0]) + " " + str(tagged_words[i+1][0])
                return s.capitalize()
        elif tagged_words[i][1] in verb_set and tagged_words[i+1][1] in noun_set: #verb + noun
            s = str(tagged_words[i][0]) + " " + str(tagged_words[i+1][0])
        elif tagged_words[i][1] in verb_set and tagged_words[i+1][1] in prep_set and tagged_words[i+2][1] in noun_set: #verb + prep + noun
            s = str(tagged_words[i][0]) + " " + str(tagged_words[i+1][0]) + " " + str(tagged_words[i+2][0])
        elif i < length-2 and tagged_words[i][1] in noun_set and tagged_words[i+1][0].lower() == 'with' and tagged_words[i+2][1] in noun_set: #noun + with + noun
            s = str(tagged_words[i][0]) + " " + str(tagged_words[i+1][0]) + " " + str(tagged_words[i+2][0])
            return s.capitalize()
        elif i < length-2 and tagged_words[i][1] in noun_set and tagged_words[i+1][1] == 'IN' and tagged_words[i+2][1] in noun_set: #noun + on + (time) 
            s = str(tagged_words[i][0])
            return s.capitalize()
        elif tagged_words[i][1] in noun_set and tagged_words[i+1][1] == 'IN' and tagged_words[i+2][1] in ['CD', 'DT']: #noun + for + number(i.e., duration) 
            s = str(tagged_words[i][0])
            return s.capitalize()
        i+=1
    
    if not s:
        text = text.lower()
        s = text.replace("schedule", "").lstrip()

    return s.capitalize()


# In[28]:


# TEST CASES
#get_nn('Birthday party on Saturday')
#get_nn('schedule meeting for one hour on Tuesday 4 p.m.')
#get_nn("meeting on thursday at 4 pm for 1 hour")
#get_nn('schedule a party for three hours and 32 minutes')
#get_nn('schedule a visit for twenty two minutes')
# get_nn('Find Korean restaurant in U District for my lunch with John next Tuesday')
# get_nn('schedule some time for me tomorrow to look for dentists')


# In[29]:


# get date and time info if exists
def extract_datetime(user_input):
    #start & end time and date
    cal = pdt.Calendar()
    now = datetime.now()
    eventTime = cal.parseDT(user_input, now)[0]
    if eventTime < now:
        #date = date + timedelta(days=1) # move to next day if schedule passes current time today
        return None
        
    date = eventTime.date()
    time = eventTime.time()
    date_time = datetime.combine(date,time)
    return date_time #date, time

#print("now: %s" % datetime.now())
#print(extract_datetime(''))
#extract_datetime('monday evening')


# In[30]:


# TEST CASES
# print(extract_datetime('schedule meeting at office'))
#print(extract_datetime('schedule meeting for one hour on Tuesday 4 pm'))
# print(extract_datetime('Find Korean restaurant in U District for my lunch with John next Tuesday'))
# print(extract_datetime('schedule a meeting for an hour and half'))


# In[33]:


# a helper function that generalizes the text
def title_text(text):
    exceptions = ["a", "an", "the","and", "but", "for", "nor", "or", "in", "to", "for", "with", "on", 
                  "at", "from", "by", "about", "as", "into", "like", "through", "after", "over", "between", 
                  "out", "against", "during", "without", "before", "under", "around", "among", "of",
                  'am', 'a.m.', 'pm', 'p.m.']
    time_pattern = ['([0-9])\s*(\W*(am)\W*)', '([0-9])\s*(\W*(a.m.)\W*)', '([0-9])*(pm)', '([0-9])\s*(\W*(p.m.)\W*)']
    output_text = ''
    for word in text.split(' '): 
        for pat in time_pattern: 
            recogize_time = re.search(pat, word.lower())
            if recogize_time:
                break
        if recogize_time:
            output_text += word.lower() + " "
        elif word in exceptions: # for words exist in the exception list
            output_text += word.lower() + " "
        else: # for word need to be capitalized
            output_text += word.title() + " "
    return output_text.strip()


# In[34]:


title_text("hello")


# In[35]:


# get location or geographic info
def extract_location(user_input):
    # capitalze 
    user_input = title_text(user_input)
    text = nlp(user_input)
    tagged_words = [(word.text,word.label_) for word in text.ents]
    """
    res = ''
    #use nltk entity chunk
    nltk_tags = nltk.pos_tag(nltk.word_tokenize(user_input))
    chunks = nltk.ne_chunk(nltk_tags)
    #print(chunks)
    for n in chunks:
        if type(n) is nltk.tree.Tree:
            if (n.label() == 'GPE' or n.label() == 'ORGANIZATION'):
                l = []
                for i in n.leaves():
                    l.append(i[0])
                res = u' '.join(l)
                return res  
    """
    i = 0
    res = ''
    while i < len(tagged_words):
        if tagged_words[i][1] in {'LOC', 'FAC', 'ORG'}:
            res = tagged_words[i][0]
            return res
        i+=1

    if res == '':
        nltk_tags = nltk.pos_tag(nltk.word_tokenize(user_input))
        noun_set = {'NN', 'NNS', 'NNP', 'NNPS'}
        j = 0
        while j < (len(nltk_tags)-1):
            if nltk_tags[j][0].lower() in {'at', 'in', 'on'} and nltk_tags[j+1][1] != 'CD':
                """
                if nltk_tags[j+1][1] == 'DT' and nltk_tags[j+2][1] in noun_set:
                    res = nltk_tags[j+2][0].capitalize()
                    return res
                elif nltk_tags[j+1][1] == 'DT' and nltk_tags[j+2][1] == 'JJ' and nltk_tags[j+3][1] in noun_set:
                    res = nltk_tags[j+2][0].capitalize() + ' ' + nltk_tags[j+3][0].capitalize()
                elif nltk_tags[j+1][1] in noun_set:
                    res = nltk_tags[j+1][0].capitalize()
                    return res
                """
                res = generate_query(nltk_tags, j+1)
                break
            j+=1

    if res == '':
        res = 'geograohic info of user\'s device'
        
    return res


# In[37]:


# TEST CASES
#extract_location('have a dinner with Patrick at Panda Express')
extract_location('Find Korean restaurant in U District for my lunch with John on next Tuesday')
#extract_location('schedule dinner with John next tuesday at a Korean restaurant in U district')
#extract_location('schedule a party on sunday for two hours')


# In[49]:


import pandas as pd
#Return the time if not provided
# path = "cal_corpus.csv"
path = join(dirname(__file__), "cal_corpus.csv")
def get_time_not_provided(event):
  #drive.mount('/gdrive') ## mounting google drive
  cal_corpus = pd.read_csv(path, sep = ',')
  for i in range(0,len(cal_corpus)):
    activity = cal_corpus['activity'][i]
    if activity.lower() in event.lower():
      start_time = datetime.now().replace(hour=cal_corpus['start_hour'][i], minute=cal_corpus['start_min'][i], second = 0).strftime('%Y-%m-%d, %H:%M:%S')  #cal_corpus['start'][i]
      duration = cal_corpus['duration'][i]
      end_time = datetime.now().replace(hour=cal_corpus['end_hour'][i], minute=cal_corpus['end_min'][i], second = 0).strftime('%Y-%m-%d, %H:%M:%S')  #cal_corpus[' end'][i]
      return duration, start_time, end_time
  return None, None, None


# In[50]:


""" Smart and Anthony are working to make BERT tokenizer work
#https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
def get_nn(text):

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    tokens = tokenizer.tokenize(text)
    pos = nltk.pos_tag(tokens)

    doc = nlp(text)
    tagged_words = [(token, token.tag_) for token in doc]

    noun_set = {'NN', 'NNS', 'NNP', 'NNPS'}
    verb_set = {'VB', 'VBd', 'VBG', 'VBN', 'VBP', 'VPZ'}
    avoid_set = {'schedule', 'add', 'minutes', 'minute', 'hour', 'hours'}

    s = '' #VB NN or NN NN

    length = len(tagged_words)
    i = 0
    while i < length-1:
        if str(tagged_words[i][0]).lower() in avoid_set:
            i +=1  
            s = ""
            continue
        
        if tagged_words[i][1] in noun_set and tagged_words[i+1][1] in noun_set:
            s = str(tagged_words[i][0]) + " " + str(tagged_words[i+1][0])
            return s.capitalize()
        elif tagged_words[i][1] in verb_set and tagged_words[i+1][1] in noun_set:
            s = str(tagged_words[i][0]) + " " + str(tagged_words[i+1][0])
        elif i < length-2 and tagged_words[i][1] in noun_set and tagged_words[i+1][1] == 'IN' and tagged_words[i+2][1] in noun_set:
            s = str(tagged_words[i][0]) + " " + str(tagged_words[i+1][0]) + " " + str(tagged_words[i+2][0])
            return s.capitalize()
        i+=1
    
    if not s:
        text = text.lower()
        s = text.replace("schedule", "").lstrip()

    return s.capitalize()
get_nn('Birthday party on Saturday')
"""


# In[51]:


# get the duration in hours and minutes
# use new patterns
from word2number import w2n
def get_duration_number(input_sentence):
    pattern = ['(\W*(for)\W*)(.*?)(\W*(hour)\W*)(and)(.*?)(\W*(minute)\W*)',
               '(\W*(for)\W*)(.*?)(\W*(hour)\W*)(and)(.*?)(\W*(half)\W*)',
               '(\W*(for)\W*)(.*?)(\W*(hour)\W*)',
               '(\W*(for)\W*)(.*?)(\W*(minute)\W*)',
               '(([a-zA-Z]+)|([0-5][0-9]))\s*(\W*(hour)\W*)(and)(.*?)(\W*(minute)\W*)',
               '(([a-zA-Z]+)|([0-5][0-9]))\s*(\W*(minute)\W*)',
               '(([a-zA-Z]+)|([0-5][0-9]))\s*(\W*(hour)\W*)']
    d = None
    for idx , pat in enumerate(pattern):
        match = re.search(pat, input_sentence)
        if match:
            d = re.split('for| and| \n', match[0])
            break       
    duration_hour, duration_min = 0, 0 
    if not d:
        return duration_hour , duration_min
    if len(d) > 1:
        d = d[1:]
    #print(d)
    flag = None       
    if d and d[0]:
        first = d[0].split()
        first_duration = 0
        for i in first:
            i = i.strip()
            if i in {'hour', 'hours'}: flag = 'hour'
            elif i in {'minute', 'minutes'}: flag = 'minute'
            elif i in {'a', 'an'}: first_duration += 1
            elif i == 'half': first_duration += 30
            else: first_duration += w2n.word_to_num(i)
        if flag == 'hour':
            duration_hour = first_duration
        else:
            duration_min = first_duration   
    if len(d) == 2 and d[1]:
        second = d[1].split()
        duration_min = 0
        for i in second:
            i = i.strip()
            if i in {'minute', 'minutes'}: continue
            elif i in {'a', 'an'}: duration_min += 1
            elif i == 'half': duration_min += 30
            else: duration_min += w2n.word_to_num(i)
    return duration_hour, duration_min


# In[52]:


# Test cases
#get_duration_number('I will have dinner for 1 hour on Tuesday at 6pm')
#get_duration_number('I will have dinner on Tuesday at 6pm for an hour')
#get_duration_number('schedule a 30 minutes meeting between 2pm to 4pm')
# get_duration_number('schedule a meeting for an hour and half between 2pm to 4pm')


# In[53]:


# set up: https://stackabuse.com/python-for-nlp-getting-started-with-the-stanfordcorenlp-library/
#!pip install pycorenlp


# In[54]:


"""
from pycorenlp import StanfordCoreNLP
import json
nlp_wrapper = StanfordCoreNLP('http://localhost:9000')
def extract_person(input_sentence):
    annot_text = nlp_wrapper.annotate(input_sentence, 
        properties={'annotators': 'ner, pos',
                    'outputFormat': 'json',
                    'timeout': 2000,})
    annot_text = json.loads(annot_text)                
    for sentence in annot_text["sentences"]:
        tagged_words = [(x['word'], x['ner']) for x in sentence["tokens"]]
    person_name = [x[0] for x in tagged_words if x[1] == 'PERSON']
    return person_name
extract_person('Find Korean restaurant in U District for my lunch with John next Tuesday')
extract_person('Schedule a meeting with Tina at office next week')
"""


# In[55]:


# get name of people in event
def get_persons_name(input_sentence):
    text = title_text(input_sentence)
    common_names = nltk.corpus.names.words()
    special_case = ['Tuesday']
    person_name = [word for word in nltk.word_tokenize(text) if word in common_names and word not in special_case]
    return person_name


# In[56]:


# get_persons_name('Find Korean restaurant in U District for my lunch with John next tuesday')


# In[57]:


#testing the duration function here
"""""
def text_to_event(input_sentence):
  ###
  ### This function TAKES IN a natural langugag sentence in
  ### the type of string and RETURNS a dictionary of the features
  ### including names of people invited, date, time, and location.
  ###
  
  doc = nlp(input_sentence)

  #get subject of the event
  subject = get_nn(input_sentence)

  # get Names of people invited to the event
  people = [X.text for X in doc.ents if X.label_ in ['PERSON']]

  # get Date and Time
  matches = datefinder.find_dates(input_sentence)
  start_time = extract_datetime(input_sentence) #, time
  
  # get Location
  location = [X.text for X in doc.ents if X.label_ in ['ORG', 'LOC', 'GPE', 'FAC']]
  if len(location) > 0:
    location = location[0]
  else:
    location = ''

  # get Virtual event
  if 'zoom' in input_sentence:
    virtual = True
  else:
    virtual = False
  
  # get duration
  print(input_sentence)
  hour, minute = get_duration_number(input_sentence)
  print(hour, minute)
  if hour != 0 and minute != 0:
    end_time = None
    if hour != 0:
        if minute != 0:
          duration = timedelta(hours=hour, minutes=minute)
          end_time = start_time + duration
        else:
          duration = timedelta(hours=hour)
          end_time = start_time + duration
    else:
        if minute != 0:
          duration = timedelta(minutes=minute)
          end_time = start_time + duration
        else:
          duration = None
          end_time = None

    if duration == None:
      seconds, start, end = get_time_not_provided(subject)
      if seconds != None:
        duration = timedelta(seconds=int(seconds))
      if start_time != None and duration !=None:
        end_time = start_time + duration
      elif start_time is None and end_time is None:
        start_time = start
        end_time = end
    #if start_time = None and duration = None and end_time = None:  
    #  new_period=no.replace(hour=23, minute=30).strftime('%Y-%m-%d')


    # get recurring event
    day = re.search(r'every (\S+)', input_sentence)
    if day != None:
        day = day.group(1)
         
         #'time': time,

    features = {'event subject': subject, 'names': people, 'start date': start_time, 'duration': duration, 'end date' : end_time, 'location': location, 'virtual event': virtual, 'recurring day': day}
   
    return features
"""


# In[58]:


# Create event w/ all information
def text_to_event(input_sentence):
  ###
  ### This function TAKES IN a natural langugag sentence in
  ### the type of string and RETURNS a dictionary of the features
  ### including names of people invited, date, time, and location.
  ###
  #print(input_sentence)
  #doc = nlp(input_sentence)

  #get subject of the event
  subject = get_nn(input_sentence)

  # get Names of people invited to the event
  #people = [X.text for X in doc.ents if X.label_ in ['PERSON']]
  people = get_persons_name(input_sentence)
  
  # get Date and Time
  matches = datefinder.find_dates(input_sentence)
  start_time = extract_datetime(input_sentence) #, time
  # get Location
  #location = [X.text for X in doc.ents if X.label_ in ['ORG', 'LOC', 'GPE', 'FAC']]
  location = extract_location(input_sentence)
  if len(location) > 0:
    location = location
  else:
    location = ''

  # get Virtual event
  if 'zoom' in input_sentence:
    virtual = True
  else:
    virtual = False

  # get duration
  #duration = re.search(r'\d+\s(([a-z]+\s)+)?(hours|hour|minutes|minute)', input_sentence)
  #if duration != None:
    #duration = duration.group(0)
    #hour = re.search(r'(([a-zA-Z]+)|([0-5][0-9]))\s* hour', input_sentence)
    #minute = re.search(r'(([a-zA-Z]+)|([0-5][0-9]))\s* minute', input_sentence)
    
    hour, minute = get_duration_number(input_sentence) # get duration
    end_time = None
    if hour != 0 and start_time != None:
        hour = int(hour)
        if minute != 0:
          minute = int(minute)
          duration = timedelta(hours=hour, minutes=minute)
          end_time = start_time + duration
        else:
          duration = timedelta(hours=hour)
          end_time = start_time + duration
    else:
        if minute != 0 and start_time != None:
          minute = int(minute)
          duration = timedelta(minutes=minute)
          end_time = start_time + duration
        else:
          duration = None
          end_time = None
    
    if duration == None or start_time is None:
      seconds, start, end = get_time_not_provided(subject)
      if seconds != None:
        duration = timedelta(seconds=int(seconds))
      if start_time != None and duration !=None:
        end_time = start_time + duration
      elif start_time is None and end_time is None:
        start_time = start
        end_time = end

    #if start_time = None and duration = None and end_time = None:  
    #  new_period=no.replace(hour=23, minute=30).strftime('%Y-%m-%d')


    # get recurring event
    day = re.search(r'every (\S+)', input_sentence)
    if day != None:
        day = day.group(1)
         
         #'time': time,

    features = {'event subject': subject, 'names': people, 'start date': start_time, 'duration': duration, 'end date' : end_time, 'location': location, 'virtual event': virtual, 'recurring day': day}
   
    return features


# In[61]:


#text_to_event('schedule meeting for one hour on Tuesday 4 p.m.')
# #text_to_event('Add grocery shopping on Monday')
# #text_to_event('meet with John at restaurant')
# text_to_event('Find Korean restaurant in U District for my lunch with John next Tuesday')
# #text_to_event('schedule a lunch with john at restaurant next friday')
# #text_to_event('schedule dinner tomorrow 4pm')
# #text_to_event('Find some time for me tomorrow to play basketball')
# #text_to_event('schedule a meeting for an hour and half between 2pm to 4pm')
# #text_to_event('find me some time to swim')
# text_to_event('Schedule some time for me tomorrow to look for dentists')


# ## **Test Cases**

# In[27]:


# #Testing the code
# #path_testCases = '/content/drive/MyDrive/Kimiya/textCases.csv' #update the path as needed
# #path_testCases = "/Users/brandonjayli/Desktop/cal_corpus.csv"
# path_testCases = "/Users/brandonjayli/Desktop/intell_agent/textCases.csv"
# inputs= pd.read_csv(path_testCases)
# for input in inputs.iterrows():
#     print(input)
#     print(text_to_event(input[1][0]))


# ## **Features Detection**

# 
# 
# *   Title (Event)
# *   Time (start, end, duration)
# *   Attendee
# *   Location
# 
# 
# 
# 
# 
