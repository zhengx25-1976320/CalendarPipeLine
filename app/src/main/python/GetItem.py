# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 15:49:12 2021

@author: chengguo2000

Amazon
"""

from selectorlib import Extractor
import json
from bs4 import BeautifulSoup
import requests, json, lxml
# from typing import Dict, List, Tuple
# import httpx
# import asyncio
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
from os.path import dirname, join
import os

# Create an Extractor by reading from the YAML file
# e = Extractor.from_yaml_file('search_results.yml')
search_result_yml = Extractor.from_yaml_file(join(dirname(__file__), "search_results.yml"))

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'From': 'personal@domain.com'
}

# Create a function of Scrape
# Amaazon

# search_keyword = "hanger"

# def searchFunc(keyword):

#     search_keyword = keywordreques

def get_amazon_results(keyword):
    search_keyword = keyword

    def scrape(url):
#         headers = {
#             'dnt': '1',
#             'upgrade-insecure-requests': '1',
#             'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
#             'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#             'sec-fetch-site': 'same-origin',
#             'sec-fetch-mode': 'navigate',
#             'sec-fetch-user': '?1',
#             'sec-fetch-dest': 'document',
#             'referer': 'https://www.amazon.com/',
#             'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
#         }
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
                           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                           "Accept-Language": "en-US,en;q=0.5",
                           "Accept-Encoding": "gzip, deflate, br",
                           "Referer": "https://www.google.com/",
                           "DNT": "1",
                           "Connection": "keep-alive",
                           "Upgrade-Insecure-Requests": "1"}



        # Download the page using requests
        print("Downloading %s"%url)
        r = requests.get(url, headers=headers)
        print(r.status_code)

        # Simple check to check if page was blocked
        if r.status_code > 500:
            if "To discuss automated access to Amazon data please contact" in r.text:
                print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
            else:
                print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
            return None

        # Pass the HTML of the page and create
        return search_result_yml.extract(r.text)

    # Prepare to scrap
    original_web = "https://www.amazon.ca/s?k="
    web_url = original_web + '+'.join(search_keyword.split(' '))
    amazon_list = []
    data = scrape(web_url)
    print(data)
    # data = scrape("https://www.amazon.co.uk/s?k=hanger&ref=nb_sb_noss")
    # data = scrape("https://www.ebay.com/sch/i.html?_nkw=hanger")
    if data:
            for product in data['products'][:15]:
                product['site'] = "Amazon"
                product['search_url'] = web_url
                print(product['url'].find("/dp/"))
                if (product['url'].find("/dp/")) > 0:
                    product["reviewLink"] = ('https://www.amazon.com/product-reviews/' + product['url'][product['url'].find("/dp/")+4:product['url'].find("/dp/")+14]+'/ref=cm_cr_arp_d_paging_btm_next_1?pageNumber=1')
                    print(product["reviewLink"])
                else:
                    product["reviewLink"] = "https://www.amazon.ca" + product["url"]
                product["url"] = "https://www.amazon.ca" + product["url"]
                print("Saving Product: %s"%product['title'])
                amazon_list.append(product)

    # print(amazon_list)

    # Put the results in order
    all_info_dict = {}
    for element in amazon_list:
        key = 'Amazon-' + str(amazon_list.index(element) + 1)
        all_info_dict[key] = element



    # Get the price of each item
    item_price_dict = {}
    for feature_key in all_info_dict:
        # print(feature_key)
        item_name = feature_key

        if ('price' in all_info_dict[feature_key]):
            price_str = all_info_dict[feature_key]['price']
            if (price_str != None):
                try:
                    price_float = float(price_str.split('$')[-1])
                    item_price_dict[item_name] = price_float
                except ValueError:
                    print("This item has no price to scrap.")

    # Sort the items by price
    item_price_dict = dict(sorted(item_price_dict.items(), key=lambda item: item[1]))
    key_info_dict = {}
    for item in item_price_dict:
        key_info_dict[item] = all_info_dict.get(item)

    # Compile the sorted results
    item_sequence_list = list(key_info_dict.keys())
    all_price_sort_dict = {}
    for item_key in key_info_dict:
#         seq_key = item_sequence_list.index(item_key)
        seq_key = 'Amazon-' + str(item_sequence_list.index(item_key) + 1)
        all_price_sort_dict[seq_key] = key_info_dict[item_key]

    # Export results

#     with open(join(os.environ["HOME"], "json_1_all_info_dict.json"), 'w') as outfile_1:
    with open(join(os.environ["HOME"], "json_1_all_info_dict.json"), 'w') as outfile_1:
        json.dump(all_info_dict, outfile_1, indent = 6)

    # Export results
    with open(join(os.environ["HOME"], "json_2_all_price_sort_dict.json"), 'w') as outfile_2:
        json.dump(all_price_sort_dict, outfile_2, indent = 6)



# Code for Ebay
def get_ebay_results(keyword):
    search_keyword = keyword
    ebay_original = "https://www.ebay.com/sch/i.html?_nkw="
    # search_keyword = input('Enter item keyword: ')
    ebay_url = ebay_original + '+'.join(search_keyword.split(' '))
    print(ebay_url)

    html = requests.get(ebay_url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')

    # print(soup)
    data = []

    for item in soup.select('.s-item__wrapper.clearfix'):
        title = item.select_one('.s-item__title').text
        link = item.select_one('.s-item__link')['href']

        try:
            condition = item.select_one('.SECONDARY_INFO').text
        except:
            condition = None

        try:
            shipping = item.select_one('.s-item__logisticsCost').text
        except:
            shipping = None

        try:
            location = item.select_one('.s-item__itemLocation').text
        except:
            location = None

        try:
            watchers_sold = item.select_one('.NEGATIVE').text
        except:
            watchers_sold = None

        if item.select_one('.s-item__etrs-badge-seller') is not None:
            top_rated = True
        else:
            top_rated = False

        try:
            bid_count = item.select_one('.s-item__bidCount').text
        except:
            bid_count = None

        try:
            bid_time_left = item.select_one('.s-item__time-left').text
        except:
            bid_time_left = None

        try:
            reviews = item.select_one('.s-item__reviews-count span').text.split(' ')[0]
        except:
            reviews = None

        try:
            exctention_buy_now = item.select_one('.s-item__purchase-options-with-icon').text
        except:
            exctention_buy_now = None

        try:
            price = item.select_one('.s-item__price').text
        except:
            price = None
            
        try:
            image = item.select_one('.s-item__image-img')["src"]
        except:
            image = None



        data.append({
            # 'item': {'title': title, 'link': link, 'price': price},
            # 'condition': condition,
            # 'top_rated': top_rated,
            # 'reviews': reviews,
            # 'watchers_or_sold': watchers_sold,
            # 'buy_now_extention': exctention_buy_now,
            # 'delivery': {'shipping': shipping, 'location': location},
            # 'bids': {'count': bid_count, 'time_left': bid_time_left},

            "site" : "Ebay",
            "title": title,
            "url": link,
            "rating": "null",
            'reviews': reviews,
            "price": price,
            "search_url": ebay_url,
            "image": image,
            "reviewLink" : link

        })


    ebay_dict = {}
    for element in data[1:20]:
        key = 'Ebay-' + str(data.index(element) + 1)
        ebay_dict[key] = element



    # Get the price of each item
        item_price_dict = {}
        for feature_key in ebay_dict:
            # print(feature_key)
            item_name = feature_key
            if ('price' in ebay_dict[feature_key]):
                price_str = ebay_dict[feature_key]['price']
                if (price_str != None):
                    try:
                        price_float = float(price_str.split('$')[-1])
                        item_price_dict[item_name] = price_float
                    except ValueError:
                        print("This item has no price to scrap.")

    # Sort the items by price
        item_price_dict = dict(sorted(item_price_dict.items(), key=lambda item: item[1]))
        key_info_dict = {}
        for item in item_price_dict:
            key_info_dict[item] = ebay_dict.get(item)


        # Compile the sorted results
        item_sequence_list = list(key_info_dict.keys())
        all_price_sort_dict = {}
        for item_key in key_info_dict:
            seq_key = 'Ebay-' + str(item_sequence_list.index(item_key) + 1)
            all_price_sort_dict[seq_key] = key_info_dict[item_key]


    with open(join(os.environ["HOME"], "json_1_all_info_dict.json"), 'r') as outfile_1:
        file_data = json.load(outfile_1)
        for element in ebay_dict:
            file_data[element] = ebay_dict[element]

    with open(join(os.environ["HOME"], "json_1_all_info_dict.json"), 'w') as outfile_1:
        json.dump(file_data, outfile_1, indent = 6)


    with open(join(os.environ["HOME"], "json_2_all_price_sort_dict.json"), 'r') as outfile_2:
        price_data = json.load(outfile_2)
        for element in all_price_sort_dict:
            price_data[element] = all_price_sort_dict[element]

    with open(join(os.environ["HOME"], "json_2_all_price_sort_dict.json"), 'w') as outfile_2:
        json.dump(price_data, outfile_2, indent = 6)



    print("done searching ebay")


#         with open(join(dirname(__file__), "json_1_all_info_dict.json"), 'w') as outfile_1:
#                     json.dump(all_info_dict, outfile_1, indent = 6)



# set up the request parameters
def get_walmart_results():
    params = {
    'api_key': '57C626C32DCE4BFCB60CC3E132193B3B',
    'search_term': search_keyword,
    'type': 'search'
    }

    # make the http GET request to BlueCart API
    api_result = requests.get('https://api.bluecartapi.com/request', params)

    # print the JSON response from BlueCart API
    with open('walmart_info.json', 'w') as outfile_4:
        json.dump(api_result.json(), outfile_4, indent = 6)
    # print(json.dumps(api_result.json()))






# get_amazon_results()
# get_ebay_results()

def printItem(item):
# e = Extractor.from_yaml_file(join(dirname(__file__), 'search_results.yml'))
#     search_result = join(dirname(__file__), "search_results.yml")
    search_result = Extractor.from_yaml_file(join(dirname(__file__), "search_results.yml"))

    return search_result



# search_keyword = input('Enter item keyword: ')
# search_keyword = "hanger"
# get_amazon_results()
# get_ebay_results()

# get_walmart_results()

    
    


