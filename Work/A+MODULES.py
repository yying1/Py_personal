from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from bs4 import BeautifulSoup
import requests
import urllib.request
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from PIL import Image
import time
from selenium.webdriver.support.ui import WebDriverWait
import os
import datetime
import logging
from dateutil.relativedelta import relativedelta


def spellcheck(Data):
    for spell in Data.split():
        for let in spell:
            if let in [",", "/", ".", "?"]:
                spell = spell.replace(let, "")
        if spell in dict.keys():
            Data = Data.replace(spell, dict[spell])
        elif spell in Tdict.keys():
            Data = Data.replace(spell, Tdict[spell])
        elif spell in Udict.keys():
            Data = Data.replace(spell, Udict[spell])
    return Data

def click_pulipoint(para,poin_type,click_position,xpath_module_text,xpath_poin):
    for ntext in para.find_next_sibling(poin_type).children:
        ptext = ntext.text
        bot.find_element_by_xpath(xpath_module_text).send_keys(ptext)
        ele = bot.find_element_by_xpath(xpath_poin)
        ele.find_elements_by_tag_name('svg')[click_position].click()
        bot.find_element_by_xpath(xpath_module_text).send_keys('\n')
        ele = bot.find_element_by_xpath(xpath_poin)
        ele.find_elements_by_tag_name('svg')[click_position].click()

def ol_or_ul(para,xpath_module_text,xpath_poin):
    try:
        click_pulipoint(para,'ol', -1, xpath_module_text, xpath_poin)
    except:
        click_pulipoint(para, 'ul', -2, xpath_module_text, xpath_poin)
    finally:
        pass

def text_box_process(paras,xpath_module_text,xpath_poin):
    for para in paras:
        ptext = para.get_text()
        ptext = spellcheck(ptext)
        if ptext != '\n':
            try:
                bot.find_element_by_xpath(xpath_module_text).send_keys(ptext.strip())
                bot.find_element_by_xpath(xpath_module_text).send_keys('\n')
            except:
                pass
        elif ptext == '\n':
            try:
                ol_or_ul(para, xpath_module_text, xpath_poin)
            except:
                pass

def try_to_click(high, process_time):
    if process_time == 10:
        raise Exception("Can't click.")
    process_time += 1
    try:
        high.click()

    except:
        time.sleep(3)
        return try_to_click(high, process_time)

def module12(ASIN, l):
    try:
        mod12 = bot.find_element_by_xpath("//span[text()='Add Module']")
        location = mod12.location["y"] - 100
        bot.execute_script("window.scrollTo(0,%d);" % location)
        try_to_click(mod12,0)
        time.sleep(2)
        try_to_click(bot.find_element_by_xpath("//h4[text()='Standard Image & Light Text Overlay']"),0)
        time.sleep(2)
        image = modinfo.find('img').get("data-src")
        if not image:
            image = modinfo.find('img').get("src")
        image_file_name = image.split('/')[-1]
        kw = modinfo.find('img').get("alt")
        # print(kw)
        if not kw:
            kw = " "
        try:
            head3 = modinfo.find('h3').text.strip()
            head3 = spellcheck(head3)
            bot.find_element_by_xpath(
                "//div[@data-module-id='module-12'][" + str(l) + "]//div[@data-component-id='title']//input").send_keys(
                head3)
        except:
            pass
        try:
            paras = modinfo.find_all('p')
            for para in paras:
                ptext = para.text.strip()
                ptext = spellcheck(ptext)
                if ptext != '\n':
                    bot.find_element_by_xpath("//div[@data-module-id='module-12'][" + str(
                        l) + "]//div[@data-component-id='description']//div[starts-with(@aria-describedby,'placeholder')]").send_keys(
                        ptext)
                    bot.find_element_by_xpath("//div[@data-module-id='module-12'][" + str(
                        l) + "]//div[@data-component-id='description']//div[starts-with(@aria-describedby,'placeholder')]").send_keys(
                        '\n')
        except:
            pass
        image_file_path = imagePath + '/Module12-image' + str(l) + image_file_name
        urllib.request.urlretrieve(image, image_file_path)
        nimg = Image.open(image_file_path)
        #print(nimg)
        #if image.split('.')[-1] == 'png':
        #    nimg = nimg.convert('RGB')
        nimg = nimg.resize((970, 300))
        nimg.save(image_file_path)
        model12 = bot.find_element_by_xpath("//div[@data-module-id='module-12'][" + str(
            l) + "]//span[contains(text(),'+ Add background image')]//parent::span//parent::button")
        location = model12.location["y"] - 100
        bot.execute_script("window.scrollTo(0,%d);" % location)
        try_to_click(model12,0)
        bot.find_element_by_xpath("//input[@type='file']").send_keys(image_file_path)
        bot.find_element_by_xpath("//input[@placeholder='Enter image keywords']").send_keys(kw)
        try_to_click(bot.find_element_by_xpath("//span[(text()='Add')]//parent::span//parent::button"),0)
    except:
        logging.info("ASIN: " + str(ASIN) + " Error in Module 12")
        pass


def module11(ASIN, k):
    try:
        mod11 = bot.find_element_by_xpath("//span[text()='Add Module']")
        location = mod11.location["y"] - 100
        bot.execute_script("window.scrollTo(0,%d);" % location)
        try_to_click(mod11,0)
        time.sleep(2)
        modin11 = bot.find_element_by_xpath("//h4[text()='Standard Image & Dark Text Overlay']")
        location = modin11.location["y"] - 100
        bot.execute_script("window.scrollTo(0,%d);" % location)
        try_to_click(modin11,0)
        try:
            head3 = modinfo.find('h3').text
            head3 = spellcheck(head3)
            bot.find_element_by_xpath(
                "//div[@data-module-id='module-11'][" + str(k) + "]//div[@data-component-id='title']//input").send_keys(
                head3)
        except:
            pass
        img = modinfo.find('img').get('data-src')
        if not img:
            img = modinfo.find('img').get("src")
        img_file_name = img.split('/')[-1]
        kw = modinfo.find('img').get('alt')
        kw = spellcheck(kw)
        if not kw:
            kw = " "
        img_file_path = imagePath + '/Module11-image' + str(k) + img_file_name
        urllib.request.urlretrieve(img, img_file_path)
        nimg = Image.open(img_file_path)
        #if img.split('.')[-1] == 'png':
        #    nimg = nimg.convert('RGB')
        nimg = nimg.resize((970, 300))
        nimg.save(img_file_path)
        model11 = bot.find_element_by_xpath("//div[@data-module-id='module-11'][" + str(
            k) + "]//span[contains(text(),'+ Add background image')]//parent::span//parent::button")
        location = model11.location["y"] - 100
        bot.execute_script("window.scrollTo(0,%d);" % location)
        try_to_click(model11,0)
        bot.find_element_by_xpath("//input[@type='file']").send_keys(img_file_path)
        bot.find_element_by_xpath("//input[@placeholder='Enter image keywords']").send_keys(kw)
        try_to_click(bot.find_element_by_xpath("//span[(text()='Add')]//parent::span//parent::button"),0)
        for para in modinfo.find_all('p'):
            ptext = para.text.strip()
            ptext = spellcheck(ptext)
            if ptext != '\n':
                bot.find_element_by_xpath("//div[@data-module-id='module-11'][" + str(
                    k) + "]//div[@data-component-id='description']//div[starts-with(@aria-describedby,'placeholder')]").send_keys(
                    ptext)
                bot.find_element_by_xpath("//div[@data-module-id='module-11'][" + str(
                    k) + "]//div[@data-component-id='description']//div[starts-with(@aria-describedby,'placeholder')]").send_keys(
                    '\n')
    except:
        logging.info("ASIN: " + str(ASIN) + " Error in Module 1")
        pass


def module10(ASIN, j):
    try:
        n = 1
        mod10 = bot.find_element_by_xpath("//span[text()='Add Module']")
        location = mod10.location["y"] - 100
        bot.execute_script("window.scrollTo(0,%d);" % location)
        try_to_click(mod10,0)
        time.sleep(2)
        try_to_click(bot.find_element_by_xpath("//h4[text()='Standard Four Image/Text Quadrant']"),0)
        time.sleep(2)
        images = modinfo.find_all('img')
        try:
            for img, n in zip(images, range(1, 5)):
                image = img.get('data-src')
                if not image:
                    image = img.get('src')
                image_file_name = image.split('/')[-1]
                if str(image)!= 'None':
                    imageky = img.get('alt')
                    if not imageky:
                        imageky = " "
                    imageky = spellcheck(imageky)
                image_file_path = imagePath + '/Module10-image-' + str(j) + image_file_name
                urllib.request.urlretrieve(image, image_file_path)
                nimg = Image.open(image_file_path)
                #if image.split('.')[-1] == 'png':
                #    nimg = nimg.convert('RGB')
                nimg = nimg.resize((135, 135))
                nimg.save(image_file_path)
                try_to_click(bot.find_element_by_xpath(
                    "//div[@data-module-id='module-10'][" + str(j) + "]//div[@data-component-id='block" + str(
                        n) + "-image']//a[@role='button']"),0)
                bot.find_element_by_xpath("//input[@type='file']").send_keys(
                    image_file_path)
                bot.find_element_by_xpath("//input[@placeholder='Enter image keywords']").send_keys(imageky)
                try_to_click(bot.find_element_by_xpath("//span[(text()='Add')]//parent::span//parent::button"),0)
        except:
            pass
        try:
            header3 = modinfo.find_all('h3')
            for head3s, n in zip(header3, range(1, 5)):
                head3 = head3s.text
                head3 = spellcheck(head3)
                bot.find_element_by_xpath(
                    "//div[@data-module-id='module-10'][" + str(j) + "]//div[@data-component-id='block" + str(
                        n) + "-header']//input").send_keys(head3)
        except:
            pass
        try:
            paras = modinfo.find_all('p')
            for para, n in zip(paras, range(1, 5)):
                ptext = para.text.strip()
                ptext = spellcheck(ptext)
                if ptext != '\n':
                    bot.find_element_by_xpath(
                        "//div[@data-module-id='module-10'][" + str(j) + "]//div[@data-component-id='block" + str(
                            n) + "-description']//div[starts-with(@aria-describedby,'placeholder')]").send_keys(ptext)
                    bot.find_element_by_xpath(
                        "//div[@data-module-id='module-10'][" + str(j) + "]//div[@data-component-id='block" + str(
                            n) + "-description']//div[starts-with(@aria-describedby,'placeholder')]").send_keys('\n')
        except:
            pass

    except:
        logging.info("ASIN: " + str(ASIN) + " Error in Module 10")
        pass


def module9(ASIN, i):
    try:
        n = 1
        mod9 = bot.find_element_by_xpath("//span[text()='Add Module']")
        location = mod9.location["y"] - 100
        bot.execute_script("window.scrollTo(0,%d);" % location)
        try_to_click(mod9, 0)
        time.sleep(2)
        try_to_click(bot.find_element_by_xpath("//h4[text()='Standard Three Images & Text']"), 0)
        time.sleep(2)
        try:
            header3 = modinfo.find("h3").get_text().strip()
            header3 = spellcheck(header3)
            bot.find_element_by_xpath(
                "//div[@data-module-id='module-9'][" + str(i) + "]//div[@data-component-id='header']//input").send_keys(
                header3)
        except:
            pass
        try:
            for img_grp in modinfo.find_all('img'):
                imagelink = img_grp.get('data-src')
                if not imagelink:
                    imagelink = img_grp.get('src')
                imagelink_file_name = imagelink.split('/')[-1]
                if str(imagelink)!= 'None':
                    imageky = img_grp.get('alt')
                    if not imageky:
                        imageky = " "
                    imageky = spellcheck(imageky)
                    imagelink_file_path = imagePath + '/Module9-image-' + str(i) + imagelink_file_name
                    urllib.request.urlretrieve(imagelink, imagelink_file_path)
                    nimg = Image.open(imagelink_file_path)
                    #if imagelink.split('.')[-1] == 'png':
                    #    nimg = nimg.convert('RGB')
                    nimg = nimg.resize((300, 300))
                    nimg.save(imagelink_file_path)
                    try_to_click(bot.find_element_by_xpath(
                        "//div[@data-module-id='module-9'][" + str(i) + "]//div[@data-component-id='section" + str(
                            n) + "-image']//a[@role='button']"), 0)
                    bot.find_element_by_xpath("//input[@type='file']").send_keys(
                        imagelink_file_path)
                    bot.find_element_by_xpath("//input[@placeholder='Enter image keywords']").send_keys(imageky)
                    try_to_click(bot.find_element_by_xpath("//span[(text()='Add')]//parent::span//parent::button"), 0)
                    n += 1
        except:
            pass
        try:
            n = 1
            for head4_grp in modinfo.find_all('h4', class_='a-spacing-mini'):
                header4 = head4_grp.get_text().strip()
                header4 = spellcheck(header4)
                bot.find_element_by_xpath(
                    "//div[@data-module-id='module-9'][" + str(i) + "]//div[@data-component-id='section" + str(
                        n) + "-header']//input").send_keys(header4)
                n += 1
        except:
            pass
        try:
            for paras, n in zip(modinfo.find_all('td', class_='apm-top'), range(1, 4)):
                xpath_module_text = "//div[@data-module-id='module-9'][" + str(
                    i) + "]//div[@data-component-id='description" + str(
                    n) + "']//div[starts-with(@aria-describedby,'placeholder')]"
                xpath_poin = "//div[@data-module-id='module-9'][" + str(
                    i) + "]//div[@data-component-id='description" + str(
                    n) + "']"
                text_box_process(paras.find_all('p'), xpath_module_text, xpath_poin)
        except:
            pass
    except:
        logging.info("ASIN: " + str(ASIN) + " Error in Module 9")
    pass


def module8(ASIN, h):
    try:
        mod8 = bot.find_element_by_xpath("//span[text()='Add Module']")
        location = mod8.location["y"] - 100
        bot.execute_script("window.scrollTo(0,%d);" % location)
        try_to_click(mod8, 0)
        time.sleep(2)
        try_to_click(bot.find_element_by_xpath("//h4[text()='Standard Single Image & Highlights']"), 0)
        time.sleep(2)
        # modnum8 =bot.find_element_by_xpath("//div[@data-module-id='module-8'][" + str(h) + "]")
        imager = modinfo.find('div', class_="apm-leftimage")
        imageLink = imager.img.get('data-src')
        if not imageLink:
            imageLink = imager.img.get('src')
        imageLink_file_name = imageLink.split('/')[-1]
        kw = imager.img.get('alt')
        if not kw:
            kw = " "
        kw = spellcheck(kw)
        imageLink_file_path = imagePath + '/Module8-' + str(h) + imageLink_file_name
        urllib.request.urlretrieve(imageLink, imageLink_file_path)
        nimg = Image.open(imageLink_file_path)
        #if imageLink.split('.')[-1] == 'png':
        #    nimg = nimg.convert('RGB')
        nimg = nimg.resize((300, 300))
        nimg.save(imageLink_file_path)
        try_to_click(bot.find_element_by_xpath("//div[@data-component-id='main-image']//a[@role='button']"), 0)
        bot.find_element_by_xpath("//input[@type='file']").send_keys(imageLink_file_path)
        bot.find_element_by_xpath("//input[@placeholder='Enter image keywords']").send_keys(kw)
        try_to_click(bot.find_element_by_xpath("//span[(text()='Add')]//parent::span//parent::button"), 0)
        try:
            head3 = modinfo.find('h3').get_text().strip()
            head3 = spellcheck(head3)
            bot.find_element_by_xpath(
                "//div[@data-module-id='module-8'][" + str(h) + "]//div[@data-component-id='header']//input").send_keys(
                head3)
        except:
            pass
        subhead_list = modinfo.find('div', class_='apm-centerthirdcol').find_all('h5')
        description_list = modinfo.find('div', class_='apm-centerthirdcol').find_all('p')
        try:
            for head5, count in zip(subhead_list, range(len(subhead_list))):
                # for head5 in modinfo.find_all(class_='a-spacing-base'):by yuxuan
                head5 = head5.get_text().strip()
                head5 = spellcheck(head5)
                bot.find_elements_by_xpath("//div[@data-module-id='module-8'][" + str(
                    h) + "]//input[@placeholder='Enter subheadline text']")[count].send_keys(head5)
        except:
            pass
        try:
            count = 0
            for paras in description_list:
                ptext = paras.get_text().strip()
                ptext = spellcheck(ptext)
                bot.find_elements_by_xpath("//div[@data-module-id='module-8'][" + str(
                    h) + "]//div[@data-component-key='paragraph']//div[starts-with(@aria-describedby,'placeholder')]")[
                    count].send_keys(ptext)
                bot.find_elements_by_xpath("//div[@data-module-id='module-8'][" + str(
                    h) + "]//div[@data-component-key='paragraph']//div[starts-with(@aria-describedby,'placeholder')]")[
                    count].send_keys('\n')
                if str(paras.find_next_sibling())[-5:] == '</h5>':
                    count += 1
                elif str(paras.find_next_sibling())[-5:] == '</ul>' or str(paras.find_next_sibling())[-5:] == '</ol>':
                    poin_type = str(paras.find_next_sibling())[-3:-1]
                    if poin_type == 'ul':
                        click_position = -2
                    elif poin_type == 'ol':
                        click_position = -1
                    for ntext in paras.find_next_sibling(poin_type).children:
                        ptextn = ntext.text.strip()
                        bot.find_elements_by_xpath("//div[@data-module-id='module-8'][" + str(
                            h) + "]//div[@data-component-key='paragraph']//div[starts-with(@aria-describedby,'placeholder')]")[
                            count].send_keys(ptextn)
                        ele = bot.find_elements_by_xpath("//div[@data-module-id='module-8'][" + str(
                            h) + "]//div[@data-component-key='paragraph']")[count]
                        ele.find_elements_by_tag_name('svg')[click_position].click()
                        bot.find_elements_by_xpath("//div[@data-module-id='module-8'][" + str(
                            h) + "]//div[@data-component-key='paragraph']//div[starts-with(@aria-describedby,'placeholder')]")[
                            count].send_keys('\n')
                        ele.find_elements_by_tag_name('svg')[click_position].click()
        except:
            pass
        try:
            info4 = modinfo.find('div', class_='apm-rightthirdcol')
            bot.find_element_by_xpath(
                "//div[@data-module-id='module-8'][" + str(
                    h) + "]//div[@data-component-id='techspecs-header']//input").send_keys(
                info4.h4.text.strip('\n').strip())
        except:
            pass
        try:
            ulist = modinfo.find('div', class_='apm-rightthirdcol-inner').find_all('li')
            n = 0
            for lis in range(len(ulist)):
                bullets = bot.find_elements_by_xpath(
                    "//div[@data-module-id='module-8'][" + str(
                        h) + "]//input[@placeholder='Enter bullet point text']")
                bullets[n].send_keys(ulist[lis].text.strip('\n').strip())
                if lis == len(ulist) - 1:
                    break
                butt = bot.find_element_by_xpath("//div[@data-module-id='module-8'][" + str(
                    h) + "]//span[text()='+ Add bullet point']//parent::span//parent::button")
                location = butt.location["y"] - 100
                bot.execute_script("window.scrollTo(0,%d);" % location)
                try_to_click(butt, 0)
                n += 1
        except:
            pass
    except:
        logging.info("ASIN: " + str(ASIN) + " Error in Module 8")
        pass


def module7(ASIN, g):
    try:
        n = 0
        mod7 = bot.find_element_by_xpath("//span[text()='Add Module']")
        location = mod7.location["y"] - 100
        bot.execute_script("window.scrollTo(0,%d);" % location)
        try_to_click(mod7, 0)
        time.sleep(2)
        try_to_click(bot.find_element_by_xpath("//h4[text()='Standard Single Image & Specs Detail']"), 0)
        time.sleep(2)
        image = modinfo.find('img').get('data-src')
        if not image:
            image = modinfo.find('img').get('src')
        image_file_name = image.split('/')[-1]
        kw = modinfo.find('img').get('alt')
        if not kw:
            kw = " "
        image_file_path = imagePath + '/Module7-image' + str(g) + image_file_name
        urllib.request.urlretrieve(image, image_file_path)
        nimg = Image.open(image_file_path)
        #if image.split('.')[-1] == 'png':
        #    nimg = nimg.convert('RGB')
        nimg = nimg.resize((300, 300))
        nimg.save(image_file_path)
        try_to_click(bot.find_element_by_xpath("//div[@data-module-id='module-7'][" + str(
            g) + "]//div[@data-component-id='main-image']//a[@role='button']"), 0)
        bot.find_element_by_xpath("//input[@type='file']").send_keys(image_file_path)
        bot.find_element_by_xpath("//input[@placeholder='Enter image keywords']").send_keys(kw)
        try_to_click(bot.find_element_by_xpath("//span[(text()='Add')]//parent::span//parent::button"), 0)
        # by yuxuan
        try:
            header4 = modinfo.find('div', class_='apm-centerthirdcol').h4.get_text().strip()
            header4 = spellcheck(header4)
            bot.find_element_by_xpath("//div[@data-module-id='module-7'][" + str(
                g) + "]//div[@data-component-id='description-header']//input").send_keys(header4)
        except:
            pass
        # spell check
        subhead_list = modinfo.find('div', class_='apm-centerthirdcol').find_all('h5')
        description_list = modinfo.find('div', class_='apm-centerthirdcol').find_all('p')
        for head5, count in zip(subhead_list, range(len(subhead_list))):
            # for head5 in modinfo.find_all(class_='a-spacing-base'):by yuxuan
            head5 = head5.get_text().strip()
            head5 = spellcheck(head5)
            bot.find_elements_by_xpath("//div[@data-module-id='module-7'][" + str(
                g) + "]//input[@placeholder='Enter subheadline text']")[count].send_keys(head5)
        count = 0
        for paras in description_list:
            ptext = paras.get_text().strip()
            ptext = spellcheck(ptext)
            bot.find_elements_by_xpath("//div[@data-module-id='module-7'][" + str(
                g) + "]//div[@data-component-key='paragraph']//div[starts-with(@aria-describedby,'placeholder')]")[
                count].send_keys(ptext)
            bot.find_elements_by_xpath("//div[@data-module-id='module-7'][" + str(
                g) + "]//div[@data-component-key='paragraph']//div[starts-with(@aria-describedby,'placeholder')]")[
                count].send_keys('\n')
            if str(paras.find_next_sibling())[-5:] == '</h5>':
                count += 1
            elif str(paras.find_next_sibling())[-5:] == '</ul>' or str(paras.find_next_sibling())[-5:] == '</ol>':
                poin_type = str(paras.find_next_sibling())[-3:-1]
                if poin_type == 'ul':
                    click_position = -2
                elif poin_type == 'ol':
                    click_position = -1
                for ntext in paras.find_next_sibling(poin_type).children:
                    ptextn = ntext.text.strip()
                    bot.find_elements_by_xpath("//div[@data-module-id='module-7'][" + str(
                        g) + "]//div[@data-component-key='paragraph']//div[starts-with(@aria-describedby,'placeholder')]")[
                        count].send_keys(ptextn)
                    ele = bot.find_elements_by_xpath("//div[@data-module-id='module-7'][" + str(
                        g) + "]//div[@data-component-key='paragraph']")[count]
                    ele.find_elements_by_tag_name('svg')[click_position].click()
                    bot.find_elements_by_xpath("//div[@data-module-id='module-7'][" + str(
                        g) + "]//div[@data-component-key='paragraph']//div[starts-with(@aria-describedby,'placeholder')]")[
                        count].send_keys('\n')
                    ele.find_elements_by_tag_name('svg')[click_position].click()
        head4 = modinfo.find('div', class_='apm-rightthirdcol-inner').find('h4')
        head5 = modinfo.find('div', class_='apm-rightthirdcol-inner').find_all('h5')
        try:
            head4 = head4.get_text().strip()
            bot.find_element_by_xpath("//div[@data-module-id='module-7'][" + str(
                g) + "]//div[@data-component-id='techspecs-header']//input").send_keys(head4)
        except:
            pass
        try:
            header5a = head5[0].get_text().strip()
            header5a = spellcheck(header5a)
            bot.find_element_by_xpath("//div[@data-module-id='module-7'][" + str(
                g) + "]//div[@data-component-id='techspecs-list-subheader']//input").send_keys(header5a)
        except:
            pass
        # bot.find_element_by_xpath("//div[@data-module-id='module-7'][" + str(g) + "]//div[@data-component-id='techspecs-list-subheader']//input").send_keys(header5a) by yuxuan
        # ulist = modinfo.find('div',class_='apm-rightthirdcol-inner').find_all('li') by yuxuan
        ulist = modinfo.find('ul', class_='a-unordered-list a-vertical').find_all('li')
        for lis in range(len(ulist)):
            bullets = bot.find_elements_by_xpath(
                "//div[@data-module-id='module-7'][" + str(g) + "]//input[@placeholder='Enter bullet point text']")
            bullets[n].send_keys(ulist[lis].text.strip('\n').strip())
            if lis == len(ulist) - 1:
                break
            butt = bot.find_element_by_xpath("//div[@data-module-id='module-7'][" + str(
                g) + "]//span[text()='+ Add bullet point']//parent::span//parent::button")
            location = butt.location["y"] - 100
            bot.execute_script("window.scrollTo(0,%d);" % location)
            try_to_click(butt, 0)
            n += 1
        try:
            header5b = head5[1].get_text().strip()
            header5b = spellcheck(header5b)
            bot.find_element_by_xpath("//div[@data-module-id='module-7'][" + str(
                g) + "]//div[@data-component-id='techspecs-subheader1']//input").send_keys(header5b)
        except:
            pass

        paras = modinfo.find('div', class_='apm-rightthirdcol-inner').find_all('p')
        xpath_module_text = "//div[@data-component-id='techspecs-description1']//div[starts-with(@aria-describedby,'placeholder')]"
        xpath_poin = "//div[@data-component-id='techspecs-description1']"
        text_box_process(paras, xpath_module_text, xpath_poin)
        # for para in paras:
        #    ptext = para.get_text()
        #    ptext = spellcheck(ptext)
        #    bot.find_element_by_xpath("//div[@data-component-id='techspecs-description1']//div[starts-with(@aria-describedby,'placeholder')]").send_keys(ptext)
        # paras = modinfo.find('div', class_='apm-rightthirdcol-inner')  # by yuxuan
    except:
        logging.info("ASIN: " + str(ASIN) + " Error in Module 7")
        pass


def module6(ASIN, f):
    try:
        n = 1
        mod6 = bot.find_element_by_xpath("//span[text()='Add Module']")
        location = mod6.location["y"] - 100
        bot.execute_script("window.scrollTo(0,%d);" % location)
        try_to_click(mod6, 0)
        time.sleep(2)
        try_to_click(bot.find_element_by_xpath("//h4[text()='Multiple Image Module A']"), 0)
        time.sleep(2)
        for imgdes, intext in zip(modinfo.find_all('div', class_="apm-hovermodule-image"),
                                  modinfo.find_all('div', class_="apm-hovermodule-slides-inner")):
            image = imgdes.img.get('data-src')
            if not image:
                image = imgdes.img.get('src')
            image_file_name = image.split('/')[-1]
            kw = imgdes.img.get('alt')
            kw = spellcheck(kw)
            if not kw:
                kw = " "
            image_file_path = imagePath + '/Module6-image-' + str(f) + image_file_name
            urllib.request.urlretrieve(image, image_file_path)
            nimg = Image.open(image_file_path)
            #if image.split('.')[-1] == 'png':
            #   nimg = nimg.convert('RGB')
            nimg = nimg.resize((300, 400))
            nimg.save(image_file_path)
            try_to_click(bot.find_element_by_xpath(
                "//div[@data-module-id='module-6'][" + str(f) + "]//div[@data-component-id='image" + str(
                    n) + "']//div[@role='button']"), 0)
            try_to_click(bot.find_element_by_xpath(
                "//div[@data-module-id='module-6'][" + str(f) + "]//div[@data-component-id='image" + str(
                    n) + "']//a[@role='button']"), 0)
            bot.find_element_by_xpath("//input[@type='file']").send_keys(
                image_file_path)
            bot.find_element_by_xpath("//input[@placeholder='Enter image keywords']").send_keys(kw)
            try_to_click(bot.find_element_by_xpath("//span[(text()='Add')]//parent::span//parent::button"), 0)
            head3 = intext.h3.text.strip()
            head3 = spellcheck(head3)
            time.sleep(2)
            bot.find_element_by_xpath(
                "//div[@data-module-id='module-6'][" + str(f) + "]//div[@data-component-id='title" + str(
                    n) + "']//input[@placeholder='Enter headline text']").send_keys(head3)
            para = intext.find_all('p')
            xpath_module_text = "//div[@data-module-id='module-6'][" + str(
                f) + "]//div[@data-component-id='description" + str(
                n) + "']//div[starts-with(@aria-describedby,'placeholder')]"
            xpath_poin = "//div[@data-module-id='module-6'][" + str(f) + "]//div[@data-component-id='description" + str(
                n) + "']"
            text_box_process(para, xpath_module_text, xpath_poin)
            n += 1
            time.sleep(1)
        try:
            count = 1
            for image_text in modinfo.find_all('p', class_="a-spacing-none"):
                subtext = image_text.get_text().strip()
                subtext = spellcheck(subtext)
                bot.find_element_by_xpath(
                    "//div[@data-module-id='module-6'][" + str(f) + "]//div[@data-component-id='caption" + str(
                        count) + "']//input").send_keys(subtext)
                count += 1
        except:
            pass
    except:
        logging.info("ASIN: " + str(ASIN) + " Error in Module 6")
        pass


def module5(ASIN, e):
    try:
        n = 1
        mod5 = bot.find_element_by_xpath("//span[text()='Add Module']")
        location = mod5.location["y"] - 100
        bot.execute_script("window.scrollTo(0,%d);" % location)
        try_to_click(mod5,0)
        time.sleep(4)
        try_to_click(bot.find_element_by_xpath("//h4[text()='Standard Comparison Chart']"),0)
        time.sleep(2)
        info1 = modinfo.find('table', class_='apm-tablemodule-table').find_all('th', class_='apm-tablemodule-image')
        # info2= modinfo.find('table',class_='apm-tablemodule-table').find_all('tr',class_='apm-tablemodule-imagerows')[1].find_all('a')
        info2 = modinfo.find('table', class_='apm-tablemodule-table').find_all('tr', class_='apm-tablemodule-imagerows')[
            1].find_all('th')
        for r, q in zip(info1, info2):
            image = r.img.get('src')
            if not image:
                image = r.img.get('data-src')
            image_file_name = image.split('/')[-1]
            kw = r.get('alt')
            if not kw:
                kw = ' '
            kw = spellcheck(kw)
            image_file_path = imagePath + '/Module5-image-' + str(e) + image_file_name
            urllib.request.urlretrieve(image, image_file_path)
            nimg = Image.open(image_file_path)
            if image.split('.')[-1] == 'png':
                nimg = nimg.convert('RGB')
            nimg = nimg.resize((150, 300))
            nimg.save(image_file_path)
            img5 = bot.find_element_by_xpath(
                "//div[@data-module-id='module-5'][" + str(e) + "]//div[@data-component-key='image']//a[@role='button']")
            location = img5.location["y"] - 100
            bot.execute_script("window.scrollTo(0,%d);" % location)
            try_to_click(img5,0)
            bot.find_element_by_xpath("//input[@type='file']").send_keys(
                image_file_path)
            bot.find_element_by_xpath("//input[@placeholder='Enter image keywords']").send_keys(kw)
            try_to_click(bot.find_element_by_xpath("//span[(text()='Add')]//parent::span//parent::button"),0)
            n += 1
            time.sleep(5)
        lis1 = []
        lis2 = []
        n = 1
        titleInfo = modinfo.find_all('tr', class_='apm-tablemodule-imagerows')
        keyval = {}
        keycount = 1
        for name in titleInfo[1].find_all('th'):
            try:
                keyval[name.a.get('href').split("/")[2]] = name.a.text.strip()
                keycount += 1
            except:
                continue
        firvals = bot.find_elements_by_xpath(
            "//div[@data-module-id='module-5'][" + str(e) + "]//input[@placeholder='Enter title']")
        seconvals = bot.find_elements_by_xpath(
            "//div[@data-module-id='module-5'][" + str(e) + "]//input[@placeholder='Enter ASIN']")
        for key, val, title, ASIN in zip(keyval.keys(), keyval.values(), firvals, seconvals):
            val = spellcheck(val)
            title.send_keys(val)
            ASIN.send_keys(key)
        tablevalues = modinfo.find('table', class_='apm-tablemodule-table').find_all('tr',
                                                                                     class_='apm-tablemodule-keyvalue')
        for sel, high in zip(tablevalues[0].find_all('td', class_='apm-tablemodule-valuecell'), bot.find_elements_by_xpath(
                "//div[@data-module-id='module-5'][" + str(e) + "]//input[@type='checkbox']")):
            if "selected" in sel['class']:
                try_to_click(high,0)
        for count in range(1, len(keyval.keys()) + 1):
            lis1.append("Data " + str(count))

        df = pd.DataFrame(index=range(len(tablevalues)), columns=lis1)
        for i, tabval in zip(range(len(tablevalues)), tablevalues):
            for j, val in zip(lis1, tabval.find_all('td', class_='apm-tablemodule-valuecell')):
                df.loc[i, j] = val.span.text.strip()
        for rowheaders in tablevalues:
            for row in rowheaders.find_all('th', class_='apm-tablemodule-keyhead'):
                lis2.append(row.span.text.strip())
        df.insert(0, column='RowHead', value=lis2)
        xlocation = bot.find_element_by_xpath(
            "//div[@data-module-id='module-5'][" + str(e) + "]//span[text()='Add metric']//parent::span//parent::button")
        bot.execute_script("arguments[0].scrollIntoView(true);", xlocation)
        for i in range(len(tablevalues)):
            abc = bot.find_element_by_xpath("//div[@data-module-id='module-5'][" + str(
                e) + "]//span[text()='Add metric']//parent::span//parent::button")
            location = abc.location["y"] - 100
            bot.execute_script("window.scrollTo(0,%d);" % location)
            try_to_click(abc,0)
            time.sleep(2)
            n = 0
            k = 0
        for ele in bot.find_elements_by_xpath("//div[@data-module-id='module-5'][" + str(
                e) + "]//div[contains(@style,'0px 14px 18px 0px') and contains(@style,'width: 16.6667%')][1]//input[@placeholder='Enter metric']"):
            ele.send_keys(df.iloc[n, 0])
            n += 1
        for k, l in zip(range(2, keycount + 1), range(1, keycount + 1)):
            eles = bot.find_elements_by_xpath("//div[@data-module-id='module-5'][" + str(
                e) + "]//div[contains(@style,'0px 14px 18px 0px') and contains(@style,'width: 16.6667%')][" + str(
                k) + "]//button")
            abcs = bot.find_elements_by_xpath("//div[@data-module-id='module-5'][" + str(
                e) + "]//div[contains(@style,'0px 14px 18px 0px') and contains(@style,'width: 16.6667%')][" + str(
                k) + "]//span//div[text()='✔']")
            defs = bot.find_elements_by_xpath("//div[@data-module-id='module-5'][" + str(
                e) + "]//div[contains(@style,'0px 14px 18px 0px') and contains(@style,'width: 16.6667%')][" + str(
                k) + "]//span//div[text()='Text']")
            xyzz = bot.find_elements_by_xpath("//div[@data-module-id='module-5'][" + str(
                e) + "]//div[contains(@style,'0px 14px 18px 0px') and contains(@style,'width: 16.6667%')][" + str(
                k) + "]//span//div[text()='(none)']")
            for p, ele, mat, des, ghi in zip(range(0, len(tablevalues)), eles, abcs, defs, xyzz):
                try_to_click(ele,0)
                # time.sleep(2)
                if df.iloc[p, l] == "✓":
                    location = mat.location["y"] - 100
                    bot.execute_script("window.scrollTo(0,%d);" % location)
                    try_to_click(mat,0)
                elif df.iloc[p, l] == "-":
                    location = ghi.location["y"] - 100
                    bot.execute_script("window.scrollTo(0,%d);" % location)
                    try_to_click(ghi,0)
                else:
                    location = des.location["y"] - 100
                    bot.execute_script("window.scrollTo(0,%d);" % location)
                    try_to_click(des,0)
                    time.sleep(2)

        for num, col in zip(lis1, range(2, keycount + 1)):
            df2 = df[num]
            mask1 = df2 != "-"
            mask2 = df2 != "✓"
            df2 = df2[mask1 & mask2]
            df2 = df2.reset_index(drop=True)
            z = 0
            # print(df2)
            for ele in bot.find_elements_by_xpath("//div[@data-module-id='module-5'][" + str(
                    e) + "]//div[contains(@style,'0px 14px 18px 0px') and contains(@style,'width: 16.6667%')][" + str(
                    col) + "]//input"):
                data = df2[z]
                data = spellcheck(data)
                ele.send_keys(data)
                z += 1


    except:
        logging.info("ASIN: " + str(ASIN) + " Error in Module 5")
        pass
            


def module4(ASIN, d):
    try:
        mod4 = bot.find_element_by_xpath("//span[text()='Add Module']")
        location = mod4.location["y"] - 100
        bot.execute_script("window.scrollTo(0,%d);" % location)
        try_to_click(mod4, 0)
        time.sleep(2)
        try_to_click(bot.find_element_by_xpath("//h4[text()='Standard Four Image & Text']"), 0)
        time.sleep(2)
        try:
            head3 = modinfo.find('h3', class_='a-spacing-small').text.strip()
            #     head3 = spellcheck(head3)
            bot.find_element_by_xpath("//div[@data-module-id='module-4'][" + str(
                d) + "]//div[@data-component-id='module-title']//input").send_keys(head3)
        except:
            pass
        n = 1
        for img_grp in modinfo.find_all('img',_class=""):
            image = img_grp.get('data-src')
            if not image:
                image = img_grp.get('src')
            image_file_name = image.split('/')[-1]
            if str(image)!= 'None':
                kw = img_grp.get('alt')
                #     kw = spellcheck(kw)
                if not kw:
                    kw = ' '
                image_file_path = imagePath + '/Module4-image-' + str(d) + str(n) +image_file_name
                urllib.request.urlretrieve(image, image_file_path)
                nimg = Image.open(image_file_path)
                # if image.split('.')[-1] == 'png':
                #     nimg = nimg.convert('RGB')
                nimg = nimg.resize((220, 220))
                nimg.save(image_file_path)
                time.sleep(2)
                try_to_click(bot.find_element_by_xpath(
                    "//div[@data-module-id='module-4'][" + str(d) + "]//div[@data-component-id='block" + str(
                        n) + "-image']//a[@role='button']"), 0)
                bot.find_element_by_xpath("//input[@type='file']").send_keys(image_file_path)
                bot.find_element_by_xpath("//input[@placeholder='Enter image keywords']").send_keys(kw)
                try_to_click(bot.find_element_by_xpath("//span[(text()='Add')]//parent::span//parent::button"), 0)
                n += 1

        n = 1
        desc = modinfo.find_all('td', class_='apm-top')
        for info in desc:
            try:
                head = info.h4.get_text().strip()
                bot.find_element_by_xpath(
                    "//div[@data-module-id='module-4'][" + str(d) + "]//div[@data-component-id='block" + str(
                        n) + "-title']//input[@placeholder='Enter headline text']").send_keys(head)
            except:
                pass
            try:
                para = info.find_all('p')
                xpath_module_text = "//div[@data-module-id='module-4'][" + str(
                    d) + "]//div[@data-component-id='block" + str(
                    n) + "-description']//div[starts-with(@aria-describedby,'placeholder')]"
                xpath_poin = "//div[@data-module-id='module-4'][" + str(d) + "]//div[@data-component-id='block" + str(
                    n) + "-description']"
                text_box_process(para, xpath_module_text, xpath_poin)
            except:
                pass
            n += 1

            # ptext = para.get_text()
            # if ptext != '\n':
            #     #     ptext = spellcheck(ptext)
            #     bot.find_element_by_xpath(
            #         "//div[@data-component-id='techspecs-description1']//div[starts-with(@aria-describedby,'placeholder')]").send_keys(
            #         ptext.strip())
            #     bot.find_element_by_xpath(
            #         "//div[@data-component-id='techspecs-description1']//div[starts-with(@aria-describedby,'placeholder')]").send_keys(
            #         '\n')
            #     ol_or_ul(para, xpath_module_text, xpath_poin)
            # n = 1
            # desc = modinfo.find_all('td', class_='apm-top')
            # for info in desc:
            #     infor = info.div.p.get_text().strip()
            #
            #     infor = spellcheck(infor)
            #     bot.find_element_by_xpath(
            #         "//div[@data-module-id='module-4'][" + str(d) + "]//div[@data-component-id='block" + str(
            #             n) + "-description']//div[starts-with(@aria-describedby,'placeholder')]").send_keys(infor)
            #     n += 1
    except:
        logging.info("ASIN: " + str(ASIN) + " Error in Module 4")
        pass


def module3(ASIN, c):
    try:
        mod3 = bot.find_element_by_xpath("//span[text()='Add Module']")
        location = mod3.location["y"] - 100
        bot.execute_script("window.scrollTo(0,%d);" % location)
        try_to_click(mod3,0)
        time.sleep(2)
        try_to_click(bot.find_element_by_xpath("//h4[text()='Standard Single Right Image']"),0)
        time.sleep(2)
        # modnum3 = bot.find_element_by_xpath("//div[@data-module-id='module-3'][" + str(c) +"]")
        try_to_click(bot.find_element_by_xpath("//div[@data-module-id='module-3'][" + str(
            c) + "]//div[@data-component-id='image']//a[@role='button']"),0)
        image3 = modinfo.find('img').get('data-src')
        if not image3:
            image3 = modinfo.find('img').get('src')
        image3_file_name = image3.split('/')[-1]
        kw = modinfo.find('img').get('alt')
        if not kw:
            kw = " "
        kw = spellcheck(kw)
        image3_file_path = imagePath + '/Module-3-image' + str(c) + image3_file_name
        urllib.request.urlretrieve(image3, image3_file_path)
        nimg = Image.open(image3_file_path)
        # if image3.split('.')[-1] == 'png':
        #     nimg = nimg.convert('RGB')
        nimg = nimg.resize((300, 300))
        nimg.save(image3_file_path)
        bot.find_element_by_xpath("//input[@type='file']").send_keys(image3_file_path)
        bot.find_element_by_xpath("//input[@placeholder='Enter image keywords']").send_keys(kw)
        try_to_click(bot.find_element_by_xpath("//span[(text()='Add')]//parent::span//parent::button"),0)
        try:
            head3 = modinfo.find('h3').text.strip()
            head3 = spellcheck(head3)
            header3 = bot.find_element_by_xpath(
                "//div[@data-module-id='module-3'][" + str(c) + "]//input[@placeholder='Enter headline text']")
            header3.send_keys(head3)
        except:
            pass
        paras = modinfo.find_all('p')
        xpath_module_text = "//div[@data-module-id='module-3'][" + str(
            c) + "]//div[@data-component-key='paragraph']//div[starts-with(@aria-describedby,'placeholder')]"
        xpath_poin = "//div[@data-module-id='module-3'][" + str(c) + "]//div[@data-component-key='paragraph']"
        text_box_process(paras, xpath_module_text, xpath_poin)

    except:
        logging.info("ASIN: " + str(ASIN) + " Error in Module 3")
        pass


def module2(ASIN, b):
    try:
        mod2 = bot.find_element_by_xpath("//span[text()='Add Module']")
        location = mod2.location["y"] - 100
        bot.execute_script("window.scrollTo(0,%d);" % location)
        try_to_click(mod2, 0)
        time.sleep(2)
        mod2 = bot.find_element_by_xpath("//h4[text()='Standard Single Left Image']")
        location = mod2.location["y"] - 100
        bot.execute_script("window.scrollTo(0,%d);" % location)
        try_to_click(mod2, 0)
        time.sleep(2)
        try_to_click(bot.find_element_by_xpath("//div[@data-module-id='module-2'][" + str(
            b) + "]//div[@data-component-id='image']//a[@role='button']"), 0)
        image3 = modinfo.find('img').get('data-src')
        if not image3:
            image3 = modinfo.find('img').get('src')

        image3_file_name = image3.split('/')[-1]
        kw = modinfo.find('img').get('alt')
        kw = spellcheck(kw)
        if not kw:
            kw = ' '
        image3_file_path = imagePath + '/Module2-image' + str(b) + image3_file_name
        urllib.request.urlretrieve(image3, image3_file_path)
        nimg = Image.open(image3_file_path)
        #if image3.split('.')[-1] == 'png':
        #    nimg = nimg.convert('RGB')
        nimg = nimg.resize((300, 300))
        nimg.save(image3_file_path)
        bot.find_element_by_xpath("//input[@type='file']").send_keys(image3_file_path)
        bot.find_element_by_xpath("//input[@placeholder='Enter image keywords']").send_keys(kw)
        try_to_click(bot.find_element_by_xpath("//span[(text()='Add')]//parent::span//parent::button"), 0)

        try:
            head3 = modinfo.find('h3').text.strip()
            head3 = spellcheck(head3)
            bot.find_element_by_xpath("//div[@data-module-id='module-2'][" + str(
                b) + "]//input[@placeholder='Enter headline text']").send_keys(head3)
        except:
            pass
        paras = modinfo.find_all('p')
        xpath_module_text = "//div[@data-module-id='module-2'][" + str(
            b) + "]//div[@data-component-id='description']//div[starts-with(@aria-describedby,'placeholder')]"
        xpath_poin = "//div[@data-module-id='module-2'][" + str(b) + "]//div[@data-component-id='description']"
        text_box_process(paras, xpath_module_text, xpath_poin)
    except:
        logging.info("ASIN: " + str(ASIN) + " Error in Module 2")
        pass


def module1(ASIN, a):
    try:
        mod1 = bot.find_element_by_xpath("//span[text()='Add Module']")
        location = mod1.location["y"] - 100
        bot.execute_script("window.scrollTo(0,%d);" % location)
        try_to_click(mod1, 0)
        time.sleep(2)
        try_to_click(bot.find_element_by_xpath("//h4[text()='Standard Single Image & Sidebar']"), 0)
        time.sleep(2)
        lima = modinfo.find('div', class_='apm-leftimage').find('img').get('data-src')
        if not lima:
            lima = modinfo.find('div', class_='apm-leftimage').find('img').get('src')
        lima_file_name = lima.split('/')[-1]
        lkw = modinfo.find('div', class_='apm-leftimage').find('img').get('alt')
        lkw = spellcheck(lkw)
        if not lkw:
            lkw = " "
        lima_file_path = imagePath + '/Module-Left-image' + str(a) + lima_file_name
        urllib.request.urlretrieve(lima, lima_file_path)
        nimg = Image.open(lima_file_path)
        #if lima.split('.')[-1] == 'png':
        #    nimg = nimg.convert('RGB')
        nimg = nimg.resize((300, 400))
        nimg.save(lima_file_path)
        try_to_click(bot.find_element_by_xpath("//div[@data-module-id='module-1'][" + str(
            a) + "]//div[@data-component-id='main-image']//a[@role='button']"), 0)
        bot.find_element_by_xpath("//input[@type='file']").send_keys(
            lima_file_path)
        bot.find_element_by_xpath("//input[@placeholder='Enter image keywords']").send_keys(lkw)
        try_to_click(bot.find_element_by_xpath("//span[(text()='Add')]//parent::span//parent::button"), 0)
        rtext = modinfo.find('div', class_='apm-leftimage').find('p').text.strip()
        rtext = spellcheck(rtext)
        bot.find_elements_by_xpath(
            "//div[@data-component-id='main-image-caption']//input[@placeholder='Enter image caption text']")[
            a - 1].send_keys(
            rtext)
        try:
            rimg = modinfo.find('div', class_='apm-rightthirdcol-inner').find('img').get('data-src')
            if not rimg:
                rimg = modinfo.find('div', class_='apm-rightthirdcol-inner').find('img').get('src')
            rimg_file_name = rimg.split('/')[-1]

            rkw = modinfo.find('div', class_='apm-rightthirdcol-inner').find('img').get('alt')
            rkw = spellcheck(rkw)
            if not rkw:
                rkw = " "
            try_to_click(bot.find_element_by_xpath("//div[@data-component-id='about-image' ]//a[@role='button']"), 0)
            img_file_path = imagePath + '/Module1-Right-image' + str(a) + rimg_file_name
            urllib.request.urlretrieve(rimg, img_file_path)
            nimg = Image.open(img_file_path)
            # if rimg.split('.')[-1] == 'png':
            #     nimg = nimg.convert('RGB')
            nimg = nimg.resize((350, 175))
            nimg.save(img_file_path)
            bot.find_element_by_xpath("//input[@type='file']").send_keys(img_file_path)
            bot.find_element_by_xpath("//input[@placeholder='Enter image keywords']").send_keys(lkw)
            try_to_click(bot.find_element_by_xpath("//span[(text()='Add')]//parent::span//parent::button"), 0)
        except:
            pass
        try:
            head3 = modinfo.find('div', class_='apm-centerthirdcol').h3.text.strip('\n').strip()
            head3 = spellcheck(head3)
            bot.find_element_by_xpath(
                "//div[@data-module-id='module-1'][" + str(a) + "]//div[@data-component-id='header']//input").send_keys(
                head3)
        except:
            pass
        try:
            head4 = modinfo.find('div', class_='apm-centerthirdcol').h4.text.strip('\n').strip()
            head4 = spellcheck(head4)
            bot.find_element_by_xpath("//div[@data-module-id='module-1'][" + str(
                a) + "]//div[@data-component-id='sub-header']//input").send_keys(head4)
        except:
            pass
        try:
            paras = modinfo.find('div', class_='apm-centerthirdcol').find_all('p')
            for para in paras:
                pltext = para.text.strip()
                pltext = spellcheck(pltext)
                if pltext != '\n':
                    bot.find_element_by_xpath("//div[@data-module-id='module-1'][" + str(
                        a) + "]//div[@data-component-id='description']//div[starts-with(@aria-describedby,'placeholder')]").send_keys(
                        pltext)
                    bot.find_element_by_xpath("//div[@data-module-id='module-1'][" + str(
                        a) + "]//div[@data-component-id='description']//div[starts-with(@aria-describedby,'placeholder')]").send_keys(
                        '\n')
        except:
            pass
        try:
            bullen = modinfo.find("div", class_="amp-centerthirdcol-listbox").find_all("li")
            for count in range(1, len(bullen)):
                click1 = bot.find_element_by_xpath("//div[@data-module-id='module-1'][" + str(
                    a) + "]//div[@data-component-id='list']//span[text()='+ Add bullet point']//parent::span//parent::button")
                location = click1.location["y"] - 100
                bot.execute_script("window.scrollTo(0,%d);" % location)
                try_to_click(click1, 0)
            for info, ele in zip(bullen, bot.find_elements_by_xpath(
                    "//div[@data-module-id='module-1'][" + str(a) + "]//div[@data-component-id='list']//input")):
                bulpnt = info.find("span", class_="a-size-base a-color-secondary").get_text().strip()
                bulpnt = spellcheck(bulpnt)
                ele.send_keys(bulpnt)
        except:
            pass
        try:
            head5 = modinfo.find('div', class_='apm-rightthirdcol-inner').find('h5').text.strip('\n').strip()
            head5 = spellcheck(head5)
            bot.find_element_by_xpath("//div[@data-module-id='module-1'][" + str(
                a) + "]//div[@data-component-id='about-header']//input").send_keys(head5)
        except:
            pass
        paras = modinfo.find('div', class_='apm-rightthirdcol-inner').find_all('p')
        xpath_module_text = "//div[@data-module-id='module-1'][" + str(
            a) + "]//div[@data-component-id='about-description']//div[starts-with(@aria-describedby,'placeholder')]"
        xpath_poin = "//div[@data-module-id='module-1'][" + str(
            a) + "]//div[@data-component-id='about-description']"
        text_box_process(paras, xpath_module_text, xpath_poin)
        try:
            lis = modinfo.find('div', class_="apm-listbox a-box a-color-alternate-background a-spacing-small").find_all(
                'li')
            for li, x in zip(lis, range(len(lis))):
                li_text = li.get_text().strip()
                li_text = spellcheck(li_text)
                bot.find_elements_by_xpath("//div[@data-module-id='module-1'][" + str(
                    a) + "]//div[@data-component-id='list2']//input[@placeholder='Enter bullet point text']")[
                    x].send_keys(li_text)
                apply_asin = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                    "//div[@data-module-id='module-1'][" + str(
                                                                        a) + "]//div[@data-component-id='list2']//span[@style='display: inline-block;']//span[text()='+ Add bullet point']")))
                apply_asin.click()
        except:
            pass
    except:
        logging.info("ASIN: " + str(ASIN) + " Error in Module 1")
        pass


def send_partner_id(langage,partner_id):
    bot.find_element_by_xpath('//*[@data-value="'+langage+'"]').click()
    time.sleep(1)
    bot.find_element_by_xpath('//*[@id="awsui-select-1"]').click()
    time.sleep(1)
    bot.find_element_by_xpath('//*[@data-value="Vendor"]').click()
    time.sleep(1)
    bot.find_elements_by_tag_name('input')[1].send_keys(partner_id)
    time.sleep(1)


root = Tk()
root.title("A+Content")
Mkt_1 = StringVar()
Mkt_2 = StringVar()


def click():
    global filename
    global Mpo
    global Mpd
    filename = filedialog.askopenfilename()
    Mpo = Mkt_1.get()
    Mpd = Mkt_2.get()
    root.destroy()



wid = root.winfo_screenwidth() / 2
heig = root.winfo_screenheight() / 2
x_cor = wid - 125
y_cor = heig - 36
root.geometry("%dx%d+%d+%d" % (440, 70, x_cor, y_cor))
frame_name = Frame(root, bg="#ADD8E6")
# label_1 = Label(frame_name,text = "Please choose a file path",height="1",bg="#D3D3D3",font="Times 16")
button_1 = Button(frame_name, text="Click file path", bg="#D3D3D3", font="Times 14", height="1", command=click)
label_2 = Label(frame_name, text="Origin", height="1", width="5", bg="#D3D3D3", font="Times 16")
label_3 = Label(frame_name, text="Destination", height="1", width="12", bg="#D3D3D3", font="Times 15")
Combo_1 = ttk.Combobox(frame_name, textvariable=Mkt_1, values=("US", "UK", "DE"), width="12")
Combo_2 = ttk.Combobox(frame_name, textvariable=Mkt_2, values=("AU", "CN", "MX", "UK", "US", "AE",'SG'), width="15")
# Combo_1.grid(row=0, column=0)
# Combo_2.grid(row=0, column=1)
# label_1.grid(row=1,column=1)
label_2.grid(row=0, column=1)
label_3.grid(row=0, column=3)
Combo_1.grid(row=0, column=2)
Combo_2.grid(row=0, column=4)
# label_1.grid(row=1,column=3)
button_1.grid(row=2, column=3)
frame_name.grid(row=0, column=0)
root.mainloop()

# Original Market Place
if Mpo == "US":
    op = "com"
    language = 'en_US'
elif Mpo == "UK":
    op = "co.uk"
    language = 'en_US'
elif Mpo == "DE":
    op = "de"
    language = 'de_DE'
# Destination market place
if Mpd == "AU":
    dmp = "au"
elif Mpd == "CN":
    dmp = "cn"
elif Mpd == "US":
    dmp = "us"
elif Mpd == "UK":
    dmp = "uk"
elif Mpd == "MX":
    dmp = "mx"
elif Mpd == "AE":
    dmp = "ae.aka"
elif Mpd == "SG":
    dmp = "sg.aka"
AList = []
TList = []
TFDict = {}
dict = {}
Udict = {}
Tdict = {}
if (Mpo == 'US') and (Mpd == "UK"):
    spelldata = pd.read_excel(filename, sheet_name='US-UK')
    for USspell, UKspell in zip(spelldata['US'], spelldata['UK']):
        dict[USspell] = UKspell
        Udict[USspell] = UKspell
        Tdict[USspell] = UKspell
elif (Mpo == 'UK') and (Mpd == "US"):
    spelldata = pd.read_excel(filename, sheet_name='UK-US')
    for UKspell, USspell in zip(spelldata['UK'], spelldata['US']):
        dict[UKspell] = USspell
        Udict[UKspell] = USspell
        Tdict[UKspell] = USspell
elif (Mpo == 'US') and (Mpd == "AE"):
    spelldata = pd.read_excel(filename, sheet_name='US-AE')
    for USspell in spelldata['US']:
        dict[USspell] = ''
        Udict[USspell] = ''
        Tdict[USspell] = ''

data = pd.read_excel(filename)
modulelist = ['module-12', 'module-11', 'module-10', 'module-9', 'module-8', 'module-7', 'module-6', 'module-5',
              'module-4', 'module-3', 'module-2', 'module-1']
dname = datetime.datetime.now().microsecond
dname = "A+ Content" + str(dname)
# creating list
bot = webdriver.Chrome()
bot.maximize_window()
bot.implicitly_wait(50)
wait = WebDriverWait(bot, 10)
for ASIN in data['ASIN']:
    ASIN = str(ASIN).strip()
    print(ASIN)

    try:
        bot.get('https://www.amazon.' + op + '/dp/' + ASIN + '?language=' + language)
        try:
            alert = bot.switch_to.alert
            alert.accept()
        except:
            pass
        time.sleep(1)
        soup = BeautifulSoup(bot.page_source, 'lxml')
        aplus_all_modules = soup.find_all('div', class_='aplus-module')

        if not aplus_all_modules:
            if os.path.exists(os.environ['USERPROFILE'] + '/Desktop/' + dname):
                logging.basicConfig(filename=os.environ['USERPROFILE'] + '/Desktop/' + dname + '/my_log.log',
                                    level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s',
                                    datefmt='%m/%d/%Y %H:%M:%S')
                logging.info("ASIN: " + str(ASIN) + " No Modules were found")
                continue
            else:
                os.makedirs(os.environ['USERPROFILE'] + '/Desktop/' + dname)
                logging.basicConfig(filename=os.environ['USERPROFILE'] + '/Desktop/' + dname + '/my_log.log',
                                    level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s',
                                    datefmt='%m/%d/%Y %H:%M:%S')
                logging.info("ASIN: " + str(ASIN) + " No Modules were found")
                continue
        # if all[0].attrs['class'][2] not in modulelist:
        #     logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s',
        #                         datefmt='%m/%d/%Y %H:%M:%S')
        #     logging.info("ASIN: " + str(ASIN) + "No Modules were found")
        #     continue
        os.makedirs(os.environ['USERPROFILE'] + '/Desktop/' + dname + '/' + ASIN)
        imagePath = os.environ['USERPROFILE'] + '/Desktop/' + dname + '/' + ASIN
        logging.basicConfig(filename=os.environ['USERPROFILE'] + '/Desktop/' + dname + '/my_log.log',
                            level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s',
                            datefmt='%m/%d/%Y %H:%M:%S')
        # logging.basicConfig(level = logging.INFO,format='%(asctime)s:%(levelname)s:%(message)s',datefmt = '%m/%d/%Y %H:%M:%S')
        logging.info("ASIN: " + str(ASIN) + " Start Time")
        start = datetime.datetime.now()
        # bot.get("https://sota-" + dmp + ".amazon.com/manager/")
        bot.get('https://sota-' + dmp + '.amazon.com/content-manager/content/new/revision/draft/edit')
        #time.sleep(40)

        apply_asin = wait.until(EC.element_to_be_clickable((By.XPATH,"//span[text()='Next: Apply ASINs']//parent::span//parent::button")))
        apply_asin_loc = bot.find_element_by_xpath("//span[text()='Next: Apply ASINs']//parent::span//parent::button")
        location = apply_asin_loc.location["y"]
        bot.execute_script("window.scrollTo(0,%d);" % location)
        apply_asin.click()
        # try_to_click(apply_asin,0)
        time.sleep(2)
        input_asin = bot.find_elements_by_tag_name('input')[2]
        input_asin.send_keys(ASIN)
        time.sleep(1)
        try_to_click(bot.find_element_by_xpath('//*[@class="awsui-select-dropdown-options-container"]'),0)
        time.sleep(1)
        # try_to_click(bot.find_element_by_xpath('//*[@class="awsui-checkbox"]'))
        time.sleep(1)
        try_to_click(bot.find_element_by_xpath('//*[@id="ApplyContentButton"]/button'),0)
        time.sleep(3)
        try_to_click(bot.find_element_by_xpath("//span[text()='Back']//parent::span//parent::button"), 0)
        time.sleep(2)
        bot.find_element_by_tag_name('input').send_keys('title')
        time.sleep(1)
        bot.find_element_by_xpath('//*[@id="awsui-select-0"]').click()
        if (Mpo == "US") and (dmp == 'cn'):
            send_partner_id('zh_CN','7937866465')
        elif (Mpo == "US") and (dmp == 'au'):
            send_partner_id('en_AU', '5951178222')
        elif (Mpo == "UK") and (dmp == 'us'):
            send_partner_id('en_US', '30271968115')
        elif (Mpo == "US") and (dmp == 'uk'):
            send_partner_id('en_GB', '17266760225')
        elif (Mpo == "US") and (dmp == 'mx'):
            send_partner_id('en_US', '21277875605')
        elif (Mpo == "US") and (dmp == 'ae.aka'):
            send_partner_id('en_AE', '14062998035')
        elif (Mpo == "UK") and (dmp == 'au'):
            send_partner_id('en_AU', '11240992922')
        elif (Mpo == "UK") and (dmp == 'cn'):
            send_partner_id('zh_CN', '9134084265')
        elif (Mpo == "DE") and (dmp == 'cn'):
            send_partner_id('zh_CN', '8302908975')
        elif (Mpo == "US") and (dmp == 'sg.aka'):
            send_partner_id('en_SG', '12781237622')
        # # time.sleep(20)
        # bot.find_element_by_xpath(
        #     "//div[@class='awsui-util-container']//button[@class='awsui-button awsui-button-variant-primary awsui-hover-child-icons']").click()
        # # if dmp == "mx":
        # #     bot.find_element_by_id("awsui-autosuggest-4").send_keys(ASIN)
        # #     bot.find_element_by_id("awsui-autosuggest-4").send_keys(Keys.ENTER)
        # # else:
        # #     bot.find_element_by_id("awsui-autosuggest-2").send_keys(ASIN)
        # #     bot.find_element_by_id("awsui-autosuggest-2").send_keys(Keys.ENTER)
        # bot.find_elements_by_tag_name('input')[-1].send_keys(ASIN)
        # bot.find_elements_by_tag_name('input')[-1].send_keys(Keys.ENTER)
        # bot.find_element_by_xpath(
        #     "//div[@class='awsui-util-p-l awsui-util-shadow']//button[@class='awsui-button awsui-button-variant-primary awsui-hover-child-icons']").click()
        a = b = c = 1
        d = e = f = 1
        g = h = i = 1
        j = k = l = 1
        for x in range(len(aplus_all_modules)):
            clasname = aplus_all_modules[x].attrs['class'][2]
            print(clasname)
            # modname = clasname.split('-')
            # modnum = modname[1]
            modinfo = aplus_all_modules[x]
            if clasname == 'module-12':
                module12(ASIN, l)
                l += 1  # n+=1
            elif clasname == 'module-11':
                module11(ASIN, k)
                k += 1
            elif clasname == 'module-10':
                module10(ASIN, j)
                j += 1
            elif clasname == 'module-9':
                module9(ASIN, i)
                i += 1
            elif clasname == 'module-8':
                module8(ASIN, h)
                h += 1
            elif clasname == 'module-7':
                module7(ASIN, g)
                g += 1
            elif clasname == 'module-6':
                module6(ASIN, f)
                f += 1
            elif clasname == 'module-5':
                module5(ASIN, e)
                e += 1
            elif clasname == 'module-4':
                module4(ASIN, d)
                d += 1
            elif clasname == 'module-3':
                module3(ASIN, c)
                c += 1
            elif clasname == 'module-2':
                module2(ASIN, b)
                b += 1
            elif clasname == 'module-1':
                module1(ASIN, a)
                a += 1


        # try:
        for button in bot.find_elements_by_tag_name('button'):
            if button.text == 'Override':
                try_to_click(button,
                             0)
                break

        time.sleep(2)
        try_to_click(bot.find_element_by_xpath("//span[text()='Save as draft']//parent::span//parent::button"),0)
        # except:
        #     try_to_click(bot.find_element_by_xpath("//span[text()='Save as draft']//parent::span//parent::button"),0)
        # bot.find_element_by_xpath("//span[text()='Save for later']//parent::span//parent::button").click()
        logging.info("ASIN: " + ASIN + " End Time")
        end = datetime.datetime.now()
        t_diff = relativedelta(end, start)
        t_delta = '{h}:{m}:{s}'.format(h=t_diff.hours, m=t_diff.minutes, s=t_diff.seconds)
        AList.append(ASIN)
        TList.append(str(t_delta))
    except:
        pass

    TFDict["ASIN"] = AList
    TFDict["Time"] = TList
    Tf = pd.DataFrame(TFDict)

    Tf.to_csv(os.environ['USERPROFILE'] + '/Desktop/' + dname + "/TimeSheet.csv", index=False)
window = Tk()
window.withdraw()
messagebox.showinfo("Completed")

def output_error(log):
    error_lines = []
    for line in log.readlines():
        if 'Error' in line:
            line= line.replace('\n','')
            error_message = line.split(':')[-1].strip()
            if error_message not in error_lines:
                error_lines.append(error_message)

    error_df = pd.DataFrame(error_lines,columns = ['error'])
    error_df.to_excel('error_message.xlsx',index = False)

log = open(os.environ['USERPROFILE'] + '/Desktop/' + dname +'/my_log.log','r',encoding='utf-8')
output_error(log)
