## Last updated on 2020-11-11 by yingyy@


def Decoder(ipt1,ipt2):
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    import time
    import pandas as pd
    from bs4 import BeautifulSoup
    import os
    import re
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    ipt1=int(ipt1)
    ipt2=int(ipt2)
    max_attr = 0
    print(max_attr)
    print(ipt1)
    print(ipt2)
    dic_attris = {1:'bullet_point',2:'product_description',3:'brand',4:'subject_keyword',5:'generic_keyword',6:'item_name'}
    dic_arcurls = {1:'na.aka.amazon.com',3:'eu.aka.amazon.com',6:'fe.aka.amazon.com',104444012:'fe.aka.amazon.com',3240:'cn.aka.amazon.com',111172:'fe.aka.amazon.com',338801:'eu.aka.amazon.com',4:'eu.aka.amazon.com',338811:'eu.aka.amazon.com',338851:'eu.aka.amazon.com',44551:'eu.aka.amazon.com',5:'eu.aka.amazon.com',35691:'eu.aka.amazon.com'}
    dic_arcids = {1:'1',3:'3',104444012:'104444012',3240:'3240',111172:'111172',338801:'338801',4:'4',6:'6',338811:'338811',338851:'338851',44551:'44551',5:'5',35691:'35691'}
    #建立字典和变量

    p = 'https://browse-query-editor-'+dic_arcurls[ipt2]+'/?browseNodeFilter=category-node-merchant-facing&catalogAttributes='+dic_attris[ipt1]+'&marketplaceId='+dic_arcids[ipt2]+'&pageSize=2000&retailAsins=N&showImages=N&useSuggestedBrowseNode=N&userQuery=&variationParentOnly=N&websiteSearchable=N'
    print(p)
    #生成完整URL
    chrome_options = Options()
    chrome_path = os.environ['USERPROFILE']+r'\AppData\Local\Google\Chrome\User Data\Default'
    chrome_options.add_argument("user-data-dir="+chrome_path)
    driver = webdriver.Chrome(options=chrome_options)
    full_url=str(p)
    driver.get(full_url)
    result_all = {}


    def get_asin_attr(asin_table_rows):
        asin_attr = {}
        global max_attr
        max_attr = 0
        for row in asin_table_rows:

            if row.find_all('td')[1].find_all(text=True):
                asin = row.find_all('td')[1].find_all(text=True)[0]
                attr = row.find_all('td')[2].find_all(text=True)
                if ' /react-text ' in attr:
                    attr = attr[1]
                elif len(attr) > max_attr:
                    max_attr = len(attr)
                asin_attr[asin] = attr
        return asin_attr

    def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]
    def upload_2000(file, sleep_time):
        try:
            upload = driver.find_element_by_xpath('//*[@id="redux-app"]/div/div[1]/div[2]/div/div/div/div[1]/div/input')
            print("upload_2000 errored, retrying")
        except:
            return upload_2000(file, sleep_time + 5)
        upload.send_keys(file)
        time.sleep(2)
        js2='document.querySelector("#redux-app > div > div.panel.panel-primary.asin-discovery-form > div.panel-collapse.collapse.in > div > div > div > div:nth-child(2) > div:nth-child(4) > div.col-xs-4.col-xs-offset-4 > button").click()'
        driver.execute_script(js2)
        ##button = driver.find_element_by_xpath('//*[@id="redux-app"]/div/div[1]/div[2]/div/div/div/div[2]/div[4]/div[2]/button').click()
        time.sleep(sleep_time)
        tab_start = 1
        result_df = []

        content = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')
        asin_table_soup = soup.find("table", {"class": "asin-list table table-bordered table-striped"})
        if asin_table_soup:
            asin_soup_body = asin_table_soup.find('tbody')
            asin_table_rows = asin_soup_body.find_all('tr')
            result = get_asin_attr(asin_table_rows)
            return result
        else:
            return upload_2000(file, sleep_time + 5)

    os.chdir(r'C:\Users\yingyy\Desktop\Catalog Update_IDQ\craw_decoder_based_on_asin__v4_RPA')
    with open('asin.txt', 'r',encoding="utf-8") as f:
        file_all = f.readlines()
    tmp_dir = r'C:\User\tmp1'
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    count = 0
    for item in chunks(file_all, 2000):
        file_path = os.path.join(tmp_dir, str(count) + 'asin')
        count += 1
        with open(file_path, 'w',encoding='utf-8') as out:
            out.writelines(item)
    print('Done file split')

    for asin_file in os.listdir(tmp_dir):
        asin_path = os.path.join(tmp_dir, asin_file)
        print(asin_path)
        time.sleep(3)
        upload_result = upload_2000(asin_path, 15)
        result_all.update(upload_result)
        os.remove(asin_path)
    lines =[]
    for key in result_all.keys():

        val = result_all[key]
        # val_list=[]

        if str(type(val)) != "<class 'bs4.element.ResultSet'>":
            # print(type(val), val)
            val =[val]

        if dic_attris[ipt1]=='bullet_point':                 
            val = [x.replace('\n', '\t') for x in val]
            # else:
            #     val_list = val
            len_val = len(val)
            if len_val < max_attr:
               val.extend([''] * (max_attr - len_val))
            line = (key,) + tuple(val)
            lines.append(line)
        else:
           
            line = (key,'; '.join(val))
           
            lines.append(line)
            
    result_excel = pd.DataFrame(lines)    
    
    def valpick(uunit):
        uunit1=[]
        for mi in uunit:
            if 'value:' in str(mi) and '"' not in str(mi):
                mi=re.findall(r'\{.*?value:(.*?) \}',str(mi))
                mi=';'.join(mi)
            elif 'value:"' in str(mi):
                mi=re.findall(r'\{.*?value:"(.*?)" \}',str(mi))
                mi=';'.join(mi)
            else:
                print('Failed')
                mi=mi 
            uunit1.append(mi)
        return uunit1
 
    result_excel=result_excel.apply(lambda x: valpick(x))
    result_excel.to_excel('result.xlsx',index=False,encoding='utf-8')
    driver.quit()


