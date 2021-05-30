import requests
import logging
import time
import csv
import itertools
import json
import pandas as pd
from multiprocessing import Pool
from ratelimiter import RateLimiter
from argparse import ArgumentParser

ASIN_HEADER = 'asin1'
DATAPATH_ATTRIBUTES = ['item_name', 'brand', 'product_description', 'generic_keyword', 'bullet_point', 'bullet_point', 'bullet_point', 'ingredients']
HTTP_STATUS_SUCCESS = 200
MAX_RETRY_ATTEMPTS = 1

rate_limiter = RateLimiter(max_calls=10, period=1)

results = []
total_results = 0
last_percent = 0

def get_datapath_info(asin):

    address = "sable-responders-adhoc-dub.amazon.com:80"
    marketplace_id = "1"
    url = 'http://{address}/datapath/query/catalog/item/-/{marketplace_id}/{asin}'.format(
    address=address, marketplace_id=marketplace_id, asin=asin)

    headers = {
            'Authorization': 'SableBasic PNCatalogDataService',
            'Accept': 'application/json',
            'Connection': 'close'
    }

    d = {}

    try:
        with rate_limiter:
            res = requests.get(url, headers=headers)
            body = res.content.decode("latin-1")
            body = body.replace("\\n"," ")
            obj = json.loads(body)
            d = obj.get("product", {})
            d['status_code'] = res.status_code
    except:
        print("Error processing ASIN:", asin)
        d['status_code'] = ""

    d['asin'] = asin
    return d

def log_result(retval):
    global last_percent

    results.append(retval)

    actual_percent = len(results) * 100 / total_results
    current_percent = round(actual_percent, 2)

    if current_percent > last_percent:
        last_percent = current_percent
        print('%.2f' % current_percent
                + "% done ( " + str(len(results)) + " / "
                + str(total_results) + " )              ", end='\r')

def process_all_asins(asins, retry_attempt):
    global results
    global total_results

    if retry_attempt >= MAX_RETRY_ATTEMPTS:
        print("Exceeded max retries. Aborting processing for " + str(len(asins)) + " ASINs.")
        return []

    total_results = len(asins)
    with Pool(processes=8) as pool:
        for asin in asins:
            pool.apply_async(get_datapath_info, args=[asin], callback=log_result)

        pool.close()
        pool.join()

    data = []
    retry_asins = []
    for item in results:
        datum = {}
        asin = item['asin']

        if item['status_code'] != HTTP_STATUS_SUCCESS:
            print("Retrying for ASIN:{}", asin)
            retry_asins.append(asin)
            continue

        datum['asin'] = asin
        counter = 0
        for attribute in DATAPATH_ATTRIBUTES:
            key = attribute
            value = ''
            if attribute == 'bullet_point':
                try:
                    value = item.get(attribute)[counter].get('value')
                except:
                    value = ''
                counter += 1
                key = key + str(counter)
            else:
                try:
                    value = item.get(attribute)[0].get('value')
                except:
                    value = ''

            if value != 'None':
                datum[key] = value
            else:
                datum[key] = ''
        data.append(datum)

    if len(retry_asins) > 0:
        retry_attempt += 1
        print("Retrying to fetch datapath attributes for " + str(len(retry_asins)) + " ASINS. Attempt number: " + str(retry_attempt))
        retried_data = process_all_asins(retry_asins, retry_attempt)
        combined_data = data + retried_data
        return combined_data

    return data

if __name__ == "__main__":

    parser = ArgumentParser(description='Download datapath attributes')
    parser.add_argument('--input_file', action='store', dest='input_file', help='input file name')
    parser.add_argument('--output_file', action='store', dest='output_file', help='output file name')
    arguments = parser.parse_args()

    print("Starting script. Parsing tsv input at " + arguments.input_file)
    df = pd.read_csv(arguments.input_file, sep='\t', encoding='latin-1')
    unique_asins = list(set(df[ASIN_HEADER].values))

    print("Number of unique ASINs:", len(unique_asins))

    datapath_attributes = process_all_asins(unique_asins, 0)

    print("Processed all ASINs. Now writing to CSV")

    datapath_df = pd.DataFrame.from_records(datapath_attributes)

    datapath_df.to_csv(arguments.output_file, sep=',', encoding='latin-1', index=False, quoting=csv.QUOTE_ALL)
    print("Created " + arguments.output_file + " and stored locally")
