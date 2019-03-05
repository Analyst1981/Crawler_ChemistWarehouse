#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import requests 
import sys
import codecs
import time
import csv
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
#引入ActionChains鼠标操作类
from selenium.webdriver.common.action_chains import ActionChains  
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



def crawl(url,keyword):  
    names=[]
    priceses=[]
    saves=[]
    #chromeOptions = webdriver.ChromeOptions()
    #chromeOptions.add_argument("--headless")
    driver= webdriver.Chrome(executable_path=(r"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")) #,chrome_options = chromeOptions
    driver.maximize_window()
    wait=ui.WebDriverWait(driver,3)
    driver.get(url)
    
    try:
        
        iframe =driver.find_element_by_xpath("//*[@id='pp_full_res']/iframe")
        driver.switch_to_frame(iframe)
        try:
            
            driver.find_element_by_xpath("/html/body/div[3]/div[6]/div[1]/a").click()
            time.sleep(2)
        except:
            try:
                driver.find_element_by_xpath("//*[@id='no-thanks']/a").click()                               
                time.sleep(2)
            except:
                driver.find_element_by_css_selector('#no-thanks > a').click()
                time.sleep(2)       
    except:
        pass
    

    
    '''       
    driver.find_element_by_xpath("//input[@id='username']").send_keys(user)
    driver.find_element_by_xpath("//input[@id='password1']").send_keys(password)
    driver.find_element_by_xpath("//input[@id='Signin']").click() 
    time.sleep(1)
    '''
    driver.find_element_by_id("p_lt_ctl02_wSB_CDN_txtWord").send_keys(keyword)
    driver.find_element_by_id("p_lt_ctl02_wSB_CDN_btnImageButton").click()    
    #time.sleep(2)
    
    button=driver.find_element_by_class_name('category-entry')
    button.click()
    try:
        num=driver.find_element_by_xpath('//*[@id="Left-Content"]/div[5]/div[1]/b').get_attribute('textContent')  
        num=num.strip()[0:3]    
    except:
        num=24
    a=0
    #Left-Content > div:nth-child(11) > div.pager-count > b
    while (a<int(num)):
        for i in range(1,9):
            for j in range(1,4):
                
                name=wait.until(lambda x:x.find_element_by_xpath('//*[@id="p_lt_ctl06_pageplaceholder_p_lt_ctl00_wPListC_lstElem"]/tbody/tr['+str(i)+']/td['+str(j)+']/a/div/div[1]/div[2]').text)                                            
                prices=wait.until(lambda x:x.find_element_by_xpath(' //*[@id="p_lt_ctl06_pageplaceholder_p_lt_ctl00_wPListC_lstElem"]/tbody/tr['+str(i)+']/td['+str(j)+']/a/div/div[2]/span[1]').text) 
                try:
                    save=wait.until(lambda x:x.find_element_by_xpath('//*[@id="p_lt_ctl06_pageplaceholder_p_lt_ctl00_wPListC_lstElem"]/tbody/tr['+str(i)+']/td['+str(j)+']/a/div/div[2]/span[2]').text)                                             
                            #save=wait.until(lambda x:x.find_element_by_css_selector('#p_lt_ctl06_pageplaceholder_p_lt_ctl00_wPListC_lstElem > tbody > tr:nth-child('+str(j)+') > td:nth-child('+str(i)+') > a > div > div.prices > span:nth-child('+str(i)+')').get_attribute('textContent'))
                except:
                    save=""
                names.append(name.strip())#split
                priceses.append(prices.strip())
                saves.append(save.strip()) 
                a+=1
                print ("%s %s %s" %(name,prices,save))
                print ("********收集%s个商品********"% a)
        try:
            s=driver.find_element_by_xpath('//*[@id="Left-Content"]/div[5]/div[2]/font/b').text
            if wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,".pager-results"),s)):
                s+=1
                ActionChains(driver).click(wait.until(lambda x: x.find_element_by_css_selector("#Left-Content > div:nth-child(11) > div.pager-results >  a:nth-child('+str(s)+')"))).perform()
        except Exception as e:
            print(str(e))
            break
        
           # wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.next-page')))
        
                
    with open(keyword+'.csv','ab+') as csvfile:
        csvfile.write(codecs.BOM_UTF8)
        writer = csv.writer(csvfile,dialect='excel')
        writer.writerow([name,prices,save])
        for s in range(0,len(names)):
            writer.writerow([names[s],priceses[s],saves[s]])
    driver.quit()
    print ("********存%s个商品********"% a)
   
def main():
    

    keies=['VitalStrength','INC', 'International Protein','Musashi','Pure Warrior','VitalStrength']
   
    start_url="https://www.chemistwarehouse.hk/"
    for key in keies:
         #key=key.decode('utf-8')#中英混输入可防止乱码
         print (key)
         target=crawl(start_url,key)
    

    
if __name__ == "__main__":
   main()
