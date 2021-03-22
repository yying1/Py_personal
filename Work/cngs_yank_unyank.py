# -*- coding: utf-8 -*-

def main(url):
    # https://maxis-service-prod-pdx.amazon.com/issues?q=status%3AOpen%20AND%20containingFolder%3A(40973237-f6b1-4117-a0ff-d9c0b9533ae9)&sort=lastUpdatedDate%20desc&rows=1000&omitPath=conversation&maxis%3Aheader%3AAmzn-Version=1.0
    # Import Packages
    # import pandas as pd
    import json
    import time
    import os
    import shutil
    import re
    from datetime import datetime
    from selenium import webdriver
    # from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import NoSuchElementException
    
    # Define a class for chrome driver for later use
    class chrome_driver(object):
        def __init__(self):
            chrome_options = Options()
            chrome_options.add_argument('disable-infobars')
            chrome_path = os.environ['USERPROFILE'] + r'\AppData\Local\Google\Chrome\User Data\Default'
            chrome_options.add_argument("user-data-dir=" + chrome_path)
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 300)
        def get_url(self,url):
            self.driver.get(url)
            while 'midway' in self.driver.current_url:
                time.sleep(20)
        def wait_click(self,element_id):
            self.wait.until(EC.element_to_be_clickable((By.ID, element_id)))
        def clickable_click(self,xpath):
            self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        def clickable_click_by_id(self,element_id):
            self.wait.until(EC.element_to_be_clickable((By.ID, element_id))).click()
        def wait_until_located(self,xpath):
            item = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            return item
        def wait_until_all_located(self,xpath):
            item_list = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
            return item_list
    
    # Function to get SIMs in the folder using maxis-service
    def get_sim_list(chrome, driver, url):
        chrome.get_url(url)
        element = driver.find_elements_by_tag_name('body')[0]
        return json.loads(element.text)['documents']
    
    
    # Function to identify if the SIM included in scope
    def is_target(sim):
        if sim['status'] != 'Open':
            return False
        if sim['createDate'] != sim['lastUpdatedConversationDate']:
            return False
        return True
    
    
    # Function to identify whether it is a yank or unyank request using keyword in the SIM title
    def get_action(sim):
        title = sim['title'].lower()
        if 'remove' in title:
            return 'yank'
        if 'yank' in title and "unyank" not in title:
            return 'yank'
        if 'unyank' in title:
            return 'unblock'
        return ''
    
    
    # Function to get reason from background in custome fields for yank/unyank
    def get_reason(sim):
        try:
            strings = sim['customFields']['string']
            for string in strings:
                if string['id'] == 'background':
                    return string['value']
            return 'unknown reason'
        except KeyError:
            return 'unknown reason'
    
    
    # Function to get all ASINs that need to be yanked/unyanked, grouped by ARC
    def get_asin_list(sim, arcs, rool):
        asin_df = {}
        for arc in arcs:
            asin_df[arc] = []
        cnt = 0
        lines = sim['description'].split('\n')
        for line in lines:
            try:
                content = rool.split(line.strip())
                asin, arc = content[0], content[1].upper()
                if len(asin) == 10:
                    if arc in arcs:
                        asin_df[arc].append(asin)
                        cnt += 1
                    elif arc == 'UK':
                        asin_df['GB'].append(asin)
                        cnt += 1
            except ValueError:
                continue
            except IndexError:
                continue
        return asin_df, cnt
    
    
    # Function to generate upload file(s) for yank/unyank per ARC
    def generate_upload_file(filename, asin_list):
        with open(filename,'w') as f:
            for asin in asin_list:
                f.writelines(asin+'\n')
    
    
    # Function to select source/destination marketplace from the dropdown on AGS webtool page
    def click_option(chrome, driver, element_id, xpath, option_text):
        chrome.clickable_click_by_id(element_id)
        time.sleep(2)
        options = driver.find_element_by_xpath(xpath).find_elements_by_tag_name('li')
        for option in options:
            if option.text == option_text:
                option.click()
                break
        time.sleep(2)
    
    
    # Function to upload a file to yank/unyank
    def upload_file(chrome, driver, agsurl, sourcemp, destmp, filename, reason):
        chrome.get_url(agsurl)
        click_option(chrome, driver, 'sourceMarketplace', '//*[@id="a-popover-1"]/div/div/ul', sourcemp)
        click_option(chrome, driver, 'destinationMarketplace', '//*[@id="a-popover-2"]/div/div/ul', destmp)
        driver.find_element_by_id('file').send_keys(filename)
        driver.find_element_by_id('reason').send_keys(reason)
        chrome.clickable_click('//*[@id="a-autoid-1"]/span/input')
        time.sleep(3)
        try:
            tracking = driver.find_element_by_xpath('//*[@id="a-page"]/div[2]/div/div[2]/div/p/a').get_attribute('href')
        except NoSuchElementException:
            tracking = ''
        return tracking
    
    
    # Function to comment on SIM and resolve SIM
    def resolve_sim(chrome, driver, simurl, comment):
        chrome.get_url(simurl)
        chrome.wait_click('issue-conversation')
        chrome.clickable_click_by_id('issue-conversation')
        driver.find_element_by_id('issue-conversation').send_keys(comment)
        chrome.clickable_click('//*[@id="issue-stream-form"]/fieldset/div[2]/div[1]/div[1]/button')
        time.sleep(5)
    
    
    # Function to create folder for SIM/upload files management
    def mkdir(path):
        path = path.strip()
        path = path.rstrip("\\")
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
    
    
    # Function to copy folders containing upload files to WorkDocs 
    def copy_folder(source_path, target_path):
        for root, dirs, files in os.walk(source_path):
            for d in dirs:
                source_folder = os.path.join(source_path, d)
                target_folder = os.path.join(target_path, d)
                mkdir(target_folder)
                for c_root, c_dirs, c_files in os.walk(source_folder):
                    for file in c_files:
                        source_file = os.path.join(source_folder, file)
                        shutil.copy(source_file, target_folder)
    
    
    # Functions to process all the SIMs that meet criteria in the SIM folder
    def process_sims(chrome, driver, sims):
        # Source marketplaces
        arcs = ['US','GB','DE','JP']
        rool = re.compile('\s+')
        # Create a folder named by current date under the same path as this script
        folder = os.getcwd()
        datestr = datetime.now().strftime('%Y%m%d')
        source_path = os.path.join(folder, datestr)
        mkdir(source_path)
        global sim_string
        sim_string = "SIM processed:"
        # Go through all open SIMs
        for sim in sims:
            # Skip the SIM if not in scope
            if not is_target(sim):
                continue
            # Skip the SIM if there is no keyword in SIM title indicating yank/unyank
            action = get_action(sim)
            if action == '':
                continue
            # Skip the SIM if no ASIN/ARC could be acraped from SIM description
            asin_df, cnt = get_asin_list(sim, arcs, rool)
            if cnt == 0:
                continue
            # Get general SIM info and create a folder named by SIM ID in the current date folder to store upload files
            requester = sim['requesterIdentity'].split(':')[-1].split('@')[0]
            simid = sim['aliases'][0]['id']
            simurl = 'https://issues.amazon.com/issues/' + simid        
            reason = requester + '@_' + simurl + '_' + get_reason(sim)
            path = os.path.join(source_path, requester+'_'+simid)
            sim_string = sim_string+simid+";"
            mkdir(path)
            # Generate and upload file(s) for each ARC, getting track id
            comment = 'Processed by Robot: '+'\n'
            for arc in arcs:
                asin_list = asin_df[arc]
                if len(asin_list) == 0:
                    continue
                filename = os.path.join(path, arc+'_'+action+'.txt')
                generate_upload_file(filename, asin_list)
                agsurl = 'https://ags.amazon.com/' + action
                tracking = upload_file(chrome, driver, agsurl, arc, 'CN', filename, reason)
                comment += tracking + '\n'
            # Do not resolve SIM if file not upload successfully
            if len(comment) == 0:
                continue
            resolve_sim(chrome, driver, simurl, comment)
        # WorkDocs path to which upload files will be copied
        # Note that WorkDocs Drive must be installed
        target_path = 'W:\\My Documents\\Yank&Unyank - RPA'
        if not os.path.exists(target_path):
            target_path = target_path.replace('My Documents','Shared With Me')
        copy_folder(source_path, target_path)
        return sim_string
    sim_string = "SIM processed:"
    chrome = chrome_driver()
    # wait = chrome.wait
    driver = chrome.driver    
    # Get open SIMs
    # URL of maxis-service to extract SIM info
    #url = 'https://maxis-service-prod-pdx.amazon.com/issues?q=status%3AOpen%20AND%20containingFolder%3A(40973237-f6b1-4117-a0ff-d9c0b9533ae9)&sort=lastUpdatedDate%20desc&rows=1000&omitPath=conversation&maxis%3Aheader%3AAmzn-Version=1.0'
    # Test folder
    # url = 'https://maxis-service-prod-pdx.amazon.com/issues?q=status%3AOpen%20AND%20containingFolder%3A(0ed4347d-a3fa-4089-ac38-330e2d6d57c0)&sort=lastUpdatedDate%20desc&rows=1000&omitPath=conversation&maxis%3Aheader%3AAmzn-Version=1.0'
    sims = get_sim_list(chrome, driver, url)
    print("get sim list done")
    # Process SIMs when the folder is not empty
    if len(sims) != 0:
        sim_string = process_sims(chrome, driver, sims)
    driver.close()
    return sim_string
    
# main('https://maxis-service-prod-pdx.amazon.com/issues?q=status%3AOpen%20AND%20containingFolder%3A(0ed4347d-a3fa-4089-ac38-330e2d6d57c0)&sort=lastUpdatedDate%20desc&rows=1000&omitPath=conversation&maxis%3Aheader%3AAmzn-Version=1.0')




