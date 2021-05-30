import sys
import csv
import codecs
import subprocess
import pandas as pd
import json
import io
import os
from multiprocessing import Pool
from argparse import ArgumentParser

amazon_API_endpoint = 'api-prod-na-us-east-1a.amazon.com'
encrypted_marketplace_id = 'A1IXFGJ6ITL7J4'

sku_header = 'seller-sku'
asin_header = 'asin1'
image_url_header = 'image-url'
midway_cookie_directory = os.path.expanduser('~/.midway/cookie')

max_retries = 3
results = []
total_results = 0
last_percent = 0

def get_asin_info(asin):
    url = 'https://api-sso-access.corp.amazon.com/{endpoint}/--/api/marketplaces/{marketplace}/products/{asin}'.format(
        endpoint=amazon_API_endpoint, marketplace=encrypted_marketplace_id, asin=asin)
    headers = 'Accept: application/vnd.com.amazon.api+json;type="product/v1"; expand="offers[].productImages(product.offer.product-images/v1)"'
    command = [
        "curl", "--anyauth", "--negotiate", "--location-trusted",
        "-u:", "-b", midway_cookie_directory,
        '--header', headers, "--header", "Accept-Language: en-US", url,
    ]

    stdout, stderr = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    ).communicate()

    try:
        # It is helpful to print out the response
        # AAPI returns errors as success messages with the error in the json
        return {
            "asin": asin,
            **json.loads(stdout.decode("latin-1"))
        }
    except:
        print(stderr.decode("latin-1"))
        print('error asin: ' + asin)
        return {
            "asin": asin,
        }

def log_result(retval):
    global last_percent

    if "error" in retval:
        return

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

    if retry_attempt >= max_retries:
        print("Exceeded max retries. Aborting processing for " + str(len(asins)) + " ASINs.")
        return {}

    total_results = len(asins)
    with Pool(processes=8) as pool:
        for asin in asins:
            pool.apply_async(get_asin_info, args=[asin], callback=log_result)

        pool.close()
        pool.join()

    print("")

    data = {}
    retry_asins = []
    for item in results:
        asin = item["asin"]
        try:
            for offer in item["entity"]["offers"]:
                for image in offer["productImages"]["entity"]["productImages"]:
                    image_type = image["variant"]
                    image_url = "https://origin-na.ssl-images-amazon.com/images/I/" + image['physicalId'] + ".jpg"
                    if asin in data:
                        curr_val = data[asin]
                        data[asin] = curr_val + ";" + image_type + ":" + image_url
                    else:
                        data[asin] = image_type + ":" + image_url
        except:
            retry_asins.append(asin)

    if len(retry_asins) > 0:
        retry_attempt += 1
        print("Retrying to fetch Image URL for " + str(len(retry_asins)) + " ASINS. Attempt number: " + str(retry_attempt))
        retried_data = process_all_asins(retry_asins, retry_attempt)
        combined_data = {**data, **retried_data}
        return combined_data

    print("No Retry needed!")
    return data

def convert_dic_to_df(dic):
    data = []
    for key,value in dic.items():
        val = {}
        val[asin_header] = key
        val[image_url_header] = value
        data.append(val)

    return pd.DataFrame(data)

if __name__ == "__main__":
    parser = ArgumentParser(description='Download Images')
    parser.add_argument('--input_file', action='store', dest='input_file', help='input file name')
    parser.add_argument('--output_file', action='store', dest='output_file', help='output file name')
    arguments = parser.parse_args()

    print("Starting script. Parsing tsv input at " + arguments.input_file)
    df = pd.read_csv(arguments.input_file, encoding='latin-1', sep='\t', dtype={sku_header: object})[[sku_header, asin_header]]

    print("Parsed file. Calling Amazon API (endpoint: " + amazon_API_endpoint + ", marketplace: " + encrypted_marketplace_id + ") for all ASINS")
    unique_asins = list(set(df[asin_header].values))
    print("No. of unique ASINs: " + str(len(unique_asins)))
    image_urls_dict = process_all_asins(unique_asins, 0)
    print("Fetched all Image URLs. Size: " + str(len(image_urls_dict)))

    print("Converting to DataFrame")
    url_df = convert_dic_to_df(image_urls_dict)

    print("Merging AmazonAPI data and input data")
    df = df.merge(right=url_df, how="left", on=asin_header)

    print("Converting to CSV")
    df.to_csv(arguments.output_file, sep=',', encoding='latin-1', index=False, quoting=csv.QUOTE_ALL)
    print("Created " + arguments.output_file + " and stored locally")

    sys.exit()
