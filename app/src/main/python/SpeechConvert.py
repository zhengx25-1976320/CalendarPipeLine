import datetime
import calendar

import spacy
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from spacy import displacy
from collections import Counter
import en_core_web_sm
import datefinder
import spacy
import re
import datetime
import time as tm
nlp = spacy.load("en_core_web_sm")

def get_nn(text):
    tokens = nltk.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    doc = nlp(text)
    pos = [(token, token.tag_) for token in doc]

    s = ''
    for p in pos:
        if s == '':
            if 'NN' in p[1]:
                s += str(p[0])
        else:
            if (p[1] == 'CN') or (p[1] == 'TM') or ('NN' in p[1]):
                s += ' '
                s += str(p[0])
            else:
                break
    return s.capitalize()

def text_to_event(input_sentence):
    ###
    ### This function TAKES IN a natural langugag sentence in
    ### the type of string and RETURNS a dictionary of the features
    ### including names of people invited, date, time, and location.
    ###
    doc = nlp(input_sentence)

    # get subject of the event
    subject = get_nn(input_sentence)

    # get Names of people invited to the event
    people = [X.text for X in doc.ents if X.label_ in ['PERSON']]

    # get Date and Time
    matches = datefinder.find_dates(input_sentence)
    time = ''
    for match in matches:
        time = match

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
        if hour != None:
            hour = int(hour.group(1))
            if minute != None:
                minute = int(minute.group(1))
                duration = datetime.timedelta(hours=hour, minutes=minute)
            else:
                duration = datetime.timedelta(hours=hour)
        else:
            if minute != None:
                minute = int(minute.group(1))
                duration = datetime.timedelta(minutes=minute)
            else:
                duration = None

        # get recurring event
        day = re.search(r'every (\S+)', input_sentence)
        if day != None:
            day = day.group(1)

        duration = duration.seconds*1000
        time = tm.mktime(time.timetuple()) * 1000
        features = {'event subject': subject, 'names': people, 'time': time, 'location': location, 'virtual event': virtual, 'recurring day': day, 'duration': duration}

        return features

def main (user_input):
#     user_input='I have lunch for 2 hours on April 30th 4:30 pm'
    features = text_to_event(user_input)
    return features