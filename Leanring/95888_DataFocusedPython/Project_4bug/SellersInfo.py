#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.client, urllib.request, urllib.parse, urllib.error, json

API_KEY = "4db2a75e63df4a1fb66f380105e4589b"

# search a list of sellers by product upc
def searchById(upc):

    # include headers and api call params
    headers = {
        'ApiGenius_API_Key': API_KEY,
    }
    
    params = urllib.parse.urlencode({
        'upc': upc,
        'api_key': '{}',
    })
    
    # connect to api and return a dict of sellers
    try:
        conn = http.client.HTTPSConnection('api.apigenius.io')
        conn.request("GET", "/products/lookup?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        conn.close()
        
        return data["items"]["pricing"]
    except Exception as e:
        print(e)
    
    return ""
        
# search a list of sellers by product name
def searchByName(name):

    # include headers and api call params
    headers = {
        'ApiGenius_API_Key': API_KEY,
    }
    
    params = urllib.parse.urlencode({
        'keyword': name,
        'title': '',
        'mpn': '',
        'category': '',
        'brand': '',
        'api_key': '',
    })
    
    # connect to api and return a dict of sellers
    try:
        conn = http.client.HTTPSConnection('api.apigenius.io')
        conn.request("GET", "/products/search?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        conn.close()
        print(data)
        return data["items"]["pricing"]
    except Exception as e:
        print(e)
    
    return ""
        
def main():
    data = searchById("194252165959")
    for d in data:
        print(d)
    data = searchByName("Fire TV Stick with Alexa Voice Remote (includes TV controls), HD streaming device")
    for d in data:
        print(d)

if __name__ == "__main__":
    main()