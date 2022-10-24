#!/usr/bin/env python
# coding: utf-8

# In[2]:


import geopy

def convert(lat, long):
    geo_locator = geopy.Nominatim(user_agent='1234')
                            # Latitude, Longitude
    r = geo_locator.reverse((lat, long))
    return r.raw['address']['postcode']
# L5J 2Y4
# print(r.raw[0]['postcode'])


# In[ ]:





# In[ ]:




