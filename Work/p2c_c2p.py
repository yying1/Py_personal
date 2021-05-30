def get_sp(asin, domain_id):
    import time
    asin = asin.strip()
    child2p_url = 'http://imsv3.amazon.com/dd/indexes/p_asinChild2Parent/' + domain_id + '/' + asin+ '/variation'
    res = wait_url(child2p_url, 1)
    p_asin = ''
    res_text = res.text
    if 'query_results:[]' in res_text:
        p_asin = ''
    else:
        try:
            p_asin = res_text.split(',')[1].replace('"', '')
            p_asin = p_asin.replace(' ','')
            p_asin = p_asin.replace('\n','')
        except:
            print(asin, domain_id, 'Get pasin wrong.')
    res.close()
    return asin+','+p_asin
def wait_url(url, s_time):
    import time
    import requests
    time.sleep(s_time)
    try:
        get_c = requests.get(url,verify=False)
        if get_c.status_code != 200:
            return wait_url(url, s_time + 1)
        else:
            return get_c
    except:
        print("faled")
        return wait_url(url, s_time)


##get imv3
def get_imv3_casin(asin,mp_id):
    import re
    print(asin)
    imv3_url = 'http://imsv3.amazon.com/dd/diagnostic/marketplaceItem/'+mp_id+'/'+asin
    r = wait_url(imv3_url, 1)
    result_c=set()
    vartion_relation = re.compile('relationships:{variation')
    if vartion_relation.search(r.text):
        return (asin,set(imv3_cpattern.findall(r.text)))
    else:
        return result_c


def p2c_c2p(mp,use_func,input_address,output_path):
    mp = int(mp)
    import time
    import requests
    from bs4 import BeautifulSoup
    import re
    from multiprocessing import Pool,freeze_support
    from functools import wraps
    from functools import partial
    mp_dict = {1: 'US', 3: 'UK', 4: 'DE', 5: 'FR', 6: 'JP', 7: 'CA', 3240: 'CN', 338851: 'TR', 35691: 'IT', 44551: 'ES', 44571: 'IN', 111172: 'AU', 218691: 'IN', 328451: 'NL', 526970: 'BR', 104444012: 'SG', 771770: 'MX'}
    domain_dict={1: 11111, 3: 33333, 4: 44444, 5: 55555, 6: 66666, 7: 77777, 3240: 26262, 338851: 300005025, 35691: 10170, 44551: 26263, 44561: 96755, 44571: 26264, 91470: 101421, 91960: 98163, 111172: 8022369, 218691: 300000032, 328451: 8043594, 526970: 8008581, 104444012: 8066252, 771770: 8022366}
    vartion_relation = re.compile('relationships:{variation')
    global imv3_cpattern
    imv3_cpattern = re.compile('child_item_id:\"(\w+)\",\$ims_attr')
    for key, val in mp_dict.items():
        print('# ' + str(key) + ':' + val)
    asin_list = []
    domain_id = str(domain_dict[mp])
    str_mp = str(mp)        
    with open(input_address, 'r',encoding='utf-8') as asins:
        for line in asins:
            line = line.strip()
            if line:
                asin_list.append(line)
    if use_func == 'p2c':
        partial_proc = partial(get_imv3_casin,mp_id= str_mp )
        result_list = map(partial_proc, asin_list)
        header = 'pasin,casin\n'
        file_name = str(mp)+'_p2c.csv'
    elif use_func == 'c2p':
        partial_proc = partial(get_sp,domain_id = domain_id)
        result_list = map(partial_proc, asin_list)
        header = 'casin,pasin\n'
        file_name = str(mp) + '_c2p.csv'
    else:
        result_list =[]
    if result_list:
        with open(output_path+file_name,'w',encoding='utf_8_sig') as output:
            output.write(header)
            for item in result_list:
                if item:
                    if type(item) == str:
                        output.write(item+'\n')
                    else:
                        asin,result_c =item
                        for casin in result_c:
                            output.write(asin+','+casin+'\n')
    return print("Done")
