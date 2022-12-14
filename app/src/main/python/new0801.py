# -*- coding: utf-8 -*-
"""R2_StatementParser.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-JjMJAtdwu713186GxSHCUjvG5KIaALd

**Command Format:**

Schedule [action] [date/time] [person] [location]
Schedule a dinner at night with John at Marriot Hotel

## **Libraries**
"""

#!pip install datefinder

#!pip install parsedatetime

#!pip install Transformers

#!pip install word2number

import datetime
import re
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer
from word2number import w2n
import spacy
nlp = spacy.load("en_core_web_sm")
import datefinder
from datetime import datetime, timedelta
import parsedatetime as pdt 
import pandas as pd
from os.path import dirname, join
#from google.colab import drive
#from pandas.core.common import random_state
#from transformers import BertTokenizer


def leaves(tree):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
        yield subtree.leaves()

def normalise(word):
    """Normalises words to lowercase and stems and lemmatizes it."""
    word = word.lower()
    # word = stemmer.stem_word(word) #if we consider stemmer then results comes with stemmed word, but in this case word will not match with comment
    word = lemmatizer.lemmatize(word)
    return word

def acceptable_word(word):
    """Checks conditions for acceptable word: length, stopword. We can increase the length if we want to consider large phrase"""
    stopwords = stopwords.words('english')
    accepted = bool(2 <= len(word) <= 40
        and word.lower() not in stopwords)
    return accepted


def get_terms(sentence):
    sentence_re = r'(?:(?:[A-Z])(?:.[A-Z])+.?)|(?:\w+(?:-\w+)*)|(?:\$?\d+(?:.\d+)?%?)|(?:...|)(?:[][.,;"\'?():-_`])'
    lemmatizer = nltk.WordNetLemmatizer()
    stemmer = nltk.stem.porter.PorterStemmer()
    grammar = r"""
        NBAR:
            {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
        
        NP:
            {<NBAR><IN><PRR>}
            {<NBAR><VBN><IN><NBAR>}
            {<NBAR><IN><NBAR>}
            {<NBAR>} # Above, connected with in/of/etc...
    """
    chunker = nltk.RegexpParser(grammar)
    toks = nltk.regexp_tokenize(sentence, sentence_re)
    postoks = nltk.tag.pos_tag(toks)
#     print(postoks)
    doc = nlp(sentence)
    verbs = [(token, token.tag_) for token in doc]
    tree = chunker.parse(verbs)
#     tree = chunker.parse(postoks)
    for leaf in leaves(tree):
        term = [str(w) for w,t in leaf]
        return term
    return []

def select_note(sentence):
    key_words = ['buy','look','find','order']
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(tok) for tok in nltk.word_tokenize(sentence)]
    lematized_sentence =  " ".join(tokens)
#     if any(re.findall(r'|'.join(key_words), lematized_sentence, re.IGNORECASE)):
#         return True, " ".join(list(get_terms(sentence)))
    for word in key_words:
        if word in lematized_sentence:
            latter_half =  sentence.split(word, 1)[1]
            noun_phrase = get_terms(latter_half)
            if len(noun_phrase) > 0:
                return True, " ".join(list(get_terms(latter_half)))
            
#     else:
    return False, ""

"""## **Clean & Tokenization**

improvemnet needs to be made: make tagged_word as a dict, consider to shorten the text for the last if, one option is to return a noun instead of the whole text
"""

#Title generator using nltk tokenizer
"""
Possible combinations that have been considered:
- noun + noun
- verb + noun
- noun + IN (with) + noun 
- noun 
"""
def get_nn(text):

    tokens = nltk.word_tokenize(text)
    pos = nltk.pos_tag(tokens)

    doc = nlp(text)
    tagged_words = [(token, token.tag_) for token in doc]
    
    noun_set = {'NN', 'NNS', 'NNP', 'NNPS','DT'} 
    verb_set = {'VB', 'VBd', 'VBG', 'VBN', 'VBP', 'VPZ'}
    avoid_set = {'schedule', 'add', 'minutes', 'minute', 'hour', 'hours'}

    s = '' #VB NN or NN NN

    length = len(tagged_words)
    i = 0
    while i < length-1:
        if str(tagged_words[i][0]).lower() in avoid_set:
            i +=1  
            continue
        
        if tagged_words[i][1] in noun_set and tagged_words[i+1][1] in noun_set: #noun + noun
            if tagged_words[i][1] == 'DT':
                s = str(tagged_words[i+1][0])
                return s.capitalize()
            else:
                s = str(tagged_words[i][0]) + " " + str(tagged_words[i+1][0])
                return s.capitalize()
        elif tagged_words[i][1] in verb_set and tagged_words[i+1][1] in noun_set: #verb +noun
            s = str(tagged_words[i][0]) + " " + str(tagged_words[i+1][0])
        elif i < length-2 and tagged_words[i][1] in noun_set and tagged_words[i+1][1] == 'IN' and tagged_words[i+2][1] in noun_set: #noun + with + noun 
            s = str(tagged_words[i][0]) + " " + str(tagged_words[i+1][0]) + " " + str(tagged_words[i+2][0]) 
            return s.capitalize()
        i+=1
    
    if not s:
        text = text.lower()
        s = text.replace("schedule", "").lstrip()


    return s.capitalize()

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

#Return the time if not provided
#path = "/content/drive/MyDrive/Kimiya/cal_corpus.csv"
#path = "/content/drive/MyDrive/calendar_code_and_doc/Kimiya/cal_corpus.csv"
def get_time_not_provided(event):
  #drive.mount('/gdrive') ## mounting google drive
  path = join(dirname(__file__), "cal_corpus.csv")
  cal_corpus = pd.read_csv(path, sep = ',')
  for i in range(0,len(cal_corpus)):
    activity = cal_corpus['activity'][i]
    if activity.lower() in event.lower():
      start_time = datetime.now().replace(hour=cal_corpus['start_hour'][i], minute=cal_corpus['start_min'][i], second = 0).strftime('%Y-%m-%d, %H:%M:%S')  #cal_corpus['start'][i]
      duration = cal_corpus['duration'][i]
      end_time = datetime.now().replace(hour=cal_corpus['end_hour'][i], minute=cal_corpus['end_min'][i], second = 0).strftime('%Y-%m-%d, %H:%M:%S')  #cal_corpus[' end'][i]
      return duration, start_time, end_time
  return None , None, None

#print(get_time_not_provided("Add Dads Birthday party on Saturday"));
#print(get_time_not_provided("Add lunch on Saturday"));

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

def get_duration_number(input_sentence):

    pattern = ['(\W*(for)\W*)(.*?)(\W*(hour)\W*)(and)(.*?)(\W*(minute)\W*)','(\W*(for)\W*)(.*?)(\W*(hour)\W*)(and)(.*?)(\W*(half)\W*)','(\W*(for)\W*)(.*?)(\W*(hour)\W*)', '(\W*(for)\W*)(.*?)(\W*(minute)\W*)', '(.*?)(\W*(hour)\W*)(and)(.*?)(\W*(minute)\W*)','(.*?)(\W*(minute)\W*)', '(.*?)(\W*(hour)\W*)']

    d = None
    for idx , pat in enumerate(pattern):
        match = re.search(pat, input_sentence)
        
        if match:
            d = re.split('for| and| \n', match[0])
            break
    
    duration_hour , duration_min = 0, 0 

    if not d:
        return duration_hour , duration_min

    if len(d) > 1:
        d = d[1:]

    print(d)
    flag = None       
 
    if d and d[0]:
        first = d[0].split()

        first_duration = 0
        for i in first:
            i = i.strip()
            if i in {'hour', 'hours'}:
                flag = 'hour'
            elif i in {'minute', 'minutes'}:
                flag = 'minute'
            elif i in {'a', 'an'}:
                first_duration += 1
            elif i == 'half':
                first_duration += 30
            else:
                first_duration += w2n.word_to_num(i)

        if flag == 'hour':
            duration_hour = first_duration
        else:
            duration_min = first_duration   

    if len(d) == 2 and d[1]:
        second = d[1].split()
        duration_min = 0
        for i in second:
            i = i.strip()
            if i in {'minute', 'minutes'}:
                continue
            elif i in {'a', 'an'}:
                duration_min += 1
            elif i == 'half':
                duration_min += 30
            else:
                duration_min += w2n.word_to_num(i)
        
    return duration_hour, duration_min

#testing the duration function here

def text_to_event(input_sentence):
    ###
    ### This function TAKES IN a natural langugag sentence in
    ### the type of string and RETURNS a dictionary of the features
    ### including names of people invited, date, time, and location.
    ###
    doc = nlp(input_sentence)
    boolean, np = select_note(input_sentence)
    print(boolean, np)
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
    #duration = re.search(r'\d+\s(([a-z]+\s)+)?(hours|hour|minutes|minute)', input_sentence)
    #if duration != None:
    #duration = duration.group(0)

    hour = re.search(r'((\d+)?) hour', input_sentence)
    minute = re.search(r'((\d+)?) minute', input_sentence)

    end_time = None
    if hour != None:
        hour = int(hour.group(1))
        if minute != None:
            minute = int(minute.group(1))
            duration = timedelta(hours=hour, minutes=minute)
            end_time = start_time + duration
        else:
            duration = timedelta(hours=hour)
            end_time = start_time + duration
    else:
        if minute != None:
            minute = int(minute.group(1))
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

    features = {'event subject': subject, 'names': people, 'start date': start_time, 'duration': duration, 'end date' : end_time, 'location': location, 'virtual event':
        virtual, 'recurring day': day, 'boolean': boolean, 'noun phrase': np}

    return features

"""## **Test Cases**"""

#Testing the code
#path_testCases = '/content/drive/MyDrive/Kimiya/textCases.csv' #update the path as needed
#inputs= pd.read_csv(path_testCases)
#for input in inputs.iterrows():
    #print(input)
    #print(text_to_event(input[1][0]))

"""## **Features Detection**

*   Title (Event)
*   Time (start, end, duration)
*   Attendee
*   Location
"""
