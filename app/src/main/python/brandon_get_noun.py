#!/usr/bin/env python
# coding: utf-8

# **Command Format:**
# 
# Schedule [action] [date/time] [person] [location]
# Schedule a dinner at night with John at Marriot Hotel
# 

# ## **Libraries**

# In[6]:





# In[1]:





# In[1]:


import datetime
import re
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
import spacy
nlp = spacy.load("en_core_web_sm")
import datefinder
from datetime import datetime, timedelta
import parsedatetime as pdt 
import pandas as pd
from os.path import dirname, join
#from google.colab import drive
from pandas.core.common import random_state
#from transformers import BertTokenizer


# ## **Clean & Tokenization**

# improvemnet needs to be made: make tagged_word as a dict, consider to shorten the text for the last if, one option is to return a noun instead of the whole text

# In[2]:


def generate_query(tagged_words, i):
    noun_set = {'NN', 'NNS', 'NNP', 'NNPS'}
    stop_words = {'to', 'for'}
    query = ''
    while i < len(tagged_words)-1:
        if (tagged_words[i][1] in noun_set) or (tagged_words[i][1] == 'IN'):
            query += str(tagged_words[i][0]) + ' '
        if str(tagged_words[i+1][0]).lower() in stop_words:
            break
        i += 1
    return query.strip()

def get_possible_query(text):
    doc = nlp(text)
    tagged_words = [(token, token.tag_) for token in doc]
    #tokens = nltk.word_tokenize(text)
    #tagged_words = nltk.pos_tag(tokens)
    #print(tagged_words)
    query_signal = {'find', 'search', 'seek', 'look'} # list words for potential query request
    noun_set = {'NN', 'NNS', 'NNP', 'NNPS', 'PRP'}
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
        if str(tagged_words[i+1][0]).lower() in stop_words:
            break
        i += 1

    if query == '':
        new_text = text
    else:
        for j in range(i+1, len(tagged_words)):
            new_text += str(tagged_words[j][0]) + ' '
    return query, new_text.strip()


# In[3]:


# TEST CASES
#get_possible_query('find me a restaurant in U district to have a lunch')
#get_possible_query('find a hospital near me for vaccine')
#get_possible_query('look for grocery in downtown to have shopping with Jim')
#get_possible_query('schedule a lunch with john at restaurant next friday')
# get_possible_query('Find some time for me tomorrow to play basketball')


# In[4]:


#Title generator using nltk tokenizer
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


# In[124]:


# TEST CASES
#get_nn('Birthday party on Saturday')
#get_nn('schedule meeting for one hour on Tuesday 4 p.m.')
#get_nn('schedule meeting for an hour on Tuesday 4 p.m.')
#get_nn("meeting on thursday at 4 pm for 1 hour")
#get_nn('schedule a party for three hours and 32 minutes')
#get_nn('schedule a visit for twenty two minutes')
#get_nn('Find Korean restaurant in U District for my lunch with John next Tuesday')
# get_nn('schedule a lunch with john at restaurant next friday')
# get_nn('Find some time for me tomorrow to play basketball')


# In[5]:


def extract_datetime(user_input):
    #start & end time and date
    cal = pdt.Calendar()
    now = datetime.now()
    eventTime = cal.parseDT(user_input, now)[0]

    if eventTime < now:
        return None

    date = eventTime.date()
    time = eventTime.time()
    date_time = datetime.combine(date,time)
    return date_time #date, time

#print("now: %s" % datetime.now())
#print(extract_datetime(''))
#extract_datetime('monday evening')


# In[6]:


# TEST CASES
# print(extract_datetime('schedule meeting at office'))
# print(extract_datetime('schedule meeting for one hour on Tuesday 4 pm'))
# print(extract_datetime('Find Korean restaurant in U District for my lunch with John next Tuesday'))
# print(extract_datetime('schedule a meeting for an hour and half between 2pm to 4pm'))


# In[7]:


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


# In[8]:


def extract_location(user_input):
    # capitalze 
    user_input = title_text(user_input)
    #print(user_input)

    text = nlp(user_input)
    tagged_words = [(word.text,word.label_) for word in text.ents]
    #print(tagged_words)
    i = 0
    res = ''
    while i < len(tagged_words):
        if tagged_words[i][1] in {'GPE', 'LOC', 'FAC', 'ORG'}:
            res = tagged_words[i][0]
            return res
        i+=1

    if res == '':
        nltk_tags = nltk.pos_tag(nltk.word_tokenize(user_input))
        noun_set = {'NN', 'NNS', 'NNP', 'NNPS'}
        j = 0
        while j < (len(nltk_tags)-1):
            if nltk_tags[j][0].lower() in {'at', 'in', 'on'}:
                if nltk_tags[j+1][1] == 'DT' and nltk_tags[j+2][1] in noun_set:
                    res = nltk_tags[j+2][0].capitalize()
                    return res
                elif nltk_tags[j+1][1] in noun_set:
                    res = nltk_tags[j+1][0].capitalize()
                    return res
            j+=1

    if res == '':
        res = "geographic info of user's device"
        
    return res


# In[9]:


# TEST CASES
# print(extract_location('have a dinner with Patrick at Panda Express'))
# print(extract_location('schedule lunch at korean restaurant'))
# print(extract_location('have breakfast at Time Bistro'))
# print(extract_location('schedule meeting at 11'))
# print(extract_location('Find Korean restaurant in U District for my lunch with John on next Tuesday'))
# print(extract_location('I will have dinner with Tina on Tuesday at 6pm for an hour'))


# In[11]:


import pandas as pd
#Return the time if not provided
path = join(dirname(__file__), "cal_corpus.csv")
#path = "/content/drive/MyDrive/calendar_code_and_doc/Kimiya/cal_corpus.csv"
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

# print(get_time_not_provided("Add Dads Birthday party on Saturday"))
# print(get_time_not_provided("Add lunch on Saturday"))
# print(get_time_not_provided("Find some time for me tomorrow to play basketball"))


# In[12]:


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


# In[13]:


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


# In[14]:


# Test cases
#get_duration_number('I will have dinner for 1 hour on Tuesday at 6pm')
#get_duration_number('I will have dinner on Tuesday at 6pm for an hour')
#get_duration_number('schedule a 30 minutes meeting between 2pm to 4pm')
# get_duration_number('schedule a meeting for an hour and half between 2pm to 4pm')


# In[15]:


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


# In[16]:


# Create event w/ all information
def text_to_event(input_sentence):
  ###
  ### This function TAKES IN a natural langugag sentence in
  ### the type of string and RETURNS a dictionary of the features
  ### including names of people invited, date, time, and location.
  ###
  print(input_sentence)
  doc = nlp(input_sentence)

  #get subject of the event
  subject = get_nn(input_sentence)

  # get Names of people invited to the event
  people = [X.text for X in doc.ents if X.label_ in ['PERSON']]
  
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


# In[17]:


#text_to_event('schedule meeting for one hour on Tuesday 4 p.m.')
#text_to_event('Add grocery shopping on Monday')
#text_to_event('meet with John at restaurant')
#text_to_event('Find Korean restaurant in U District for my lunch with John next Tuesday')
#text_to_event('schedule a lunch with john at restaurant next friday')
#text_to_event('schedule dinner tomorrow 4pm')
#text_to_event('Find some time for me tomorrow to play basketball')
# text_to_event('schedule a meeting for an hour and half between 2pm to 4pm')


# In[22]:


# print(text_to_event('find me some time tomorrow to play soccer'))
# print(text_to_event('find me some time tomorrow to look for dentist'))
# print(text_to_event('find me some time tomorrow to swim'))


# ## **Test Cases**

# In[18]:


#Testing the code
#path_testCases = '/content/drive/MyDrive/Kimiya/textCases.csv' #update the path as needed
#path_testCases = "/Users/brandonjayli/Desktop/cal_corpus.csv"
# path_testCases = "textCases.csv"
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
