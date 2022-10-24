#!/usr/bin/env python
# coding: utf-8

# In[15]:


from googleapiclient.discovery import build
# import pprint

api_key = "AIzaSyCjhqnLml2LD1pafqXroSuGr7u2-aLDqwE"
cse_id = "6b17acf25c191a3e3"

def google_search(query, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id, **kwargs).execute()
    return res['items']

def get_n_results(query, api_key, cse_id, n):
    results = google_search(query, api_key, cse_id, num = n)
    lis = []
    for result in results:
        lis.append((result['link'], result['title']))
#         pprint.pprint(result)
#     print(lis)
    return lis

def start_search(test_sentense):
#     searchable, query = select_note(test_sentense, key_words)
    searchable = True;
    if searchable == True:
        return get_n_results(test_sentense, api_key, cse_id, 5)


# In[16]:


# test = start_search(test_sentense)
# print(test)


# In[ ]:




