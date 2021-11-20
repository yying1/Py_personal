#!/usr/bin/env python
# coding: utf-8
import requests
from bs4 import BeautifulSoup
HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \AppleWebKit/537.36 (KHTML, like Gecko) \Chrome/90.0.4430.212 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})
all_reviews= []
def get_soup(url,HEADERS):
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def get_reviews(soup,all_reviews):
    reviews = soup.find_all("div",{'data-hook':'review'})

    try: 
        for item in reviews: 
            review = {
            "title": item.find("a",{'data-hook':'review-title'}).text.strip(),
            "date": item.find("span",{'data-hook':'review-date'}).text.strip(),
            "rating": item.find("i",{'data-hook':'review-star-rating'}).text.strip(),
            "review": item.find("span",{'data-hook':'review-body'}).text.strip()
            }
            all_reviews.append(review)
    except:
        pass
    
for x in range(1,101):
    soup= get_soup(f"https://www.amazon.com/product-reviews/B07JGL19WK/?ie=UTF8&reviewerType=all_reviews&pageNumber={x}",HEADERS)
    get_reviews(soup,all_reviews)
    if not soup.find("li",{'class':'a-disabled a-last'}):
        pass
    else:
        break

print(len(all_reviews))
print(*[x['title'] for x in all_reviews],sep = "\n")