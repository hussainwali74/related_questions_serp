"""
Created on 28/12/23

@author: hussainwali74

inspired by https://github.com/sundios/people-also-ask?tab=readme-ov-file (this is using selenium and did not work for me)
"""

import logging
import sys
import time
import pandas as pd
from playwright.sync_api import sync_playwright

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

query = "dogs"
clicks = 1
lang = "en"
clicks = int(clicks)

def search(query,clicks,lang):
    logging.info("new term")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.google.com?hl=" + lang)
        page.wait_for_load_state('networkidle')
        print('The keyword you selected is:', query)
        print(' Number of clicks we will do is:',clicks)
        print('Language you selected is:',lang)

        # Wait for the search box to be visible
        page.wait_for_selector("form")
        page.wait_for_selector("textarea[jsname='yZiJbe']")
        time.sleep(1)
        page.type("textarea[jsname='yZiJbe']", query)
        time.sleep(1)
        page.press("textarea[jsname='yZiJbe']", "Enter")
        time.sleep(2)
        clickingKW(clicks, page)

        browser.close()

def clickingKW(clicks, page): 
    for i in range(clicks):
        print('Clicking question #',i+1)
        try:
            # top_selector = page.query_selector_all(".related-question-pair")
            page.wait_for_selector("div[jsname='yEVEwb']")
            top_selector = page.query_selector_all("div[jsname='yEVEwb']")
            time.sleep(2)
            top_selector[i].click()
            time.sleep(2)
        except:
            continue
            raise Exception('There are no questions to Click! Index is out of Range. Please add another Keyword that contains questions')
            # top_selector = page.query_selector_all("span[jsname='r4nke']")
    
    related_queries_arr = [] 
    for top in top_selector:
        span_selector = top.query_selector("span[jsname='r4nke']")
        inner_text = span_selector.inner_text()
        inner_text = inner_text.splitlines()
    
        related_queries_arr.append(inner_text)          
    print("-------------------------------------------------------------------------")
    print(f"{related_queries_arr=}")
    print("-------------------------------------------------------------------------")
     
    df = pd.DataFrame(related_queries_arr,columns=['Questions'])

    df = df.dropna() 
    print('DataFrame is empty! There are no questions for your Keyword. Try a different keyword')
    data = [['No results. Please Try again or try a different Keyword','No Results','No Results']]
    df = pd.DataFrame(data,columns=['Questions','Sentiment','Magnitude'])
    print(df)

    print(df)
    df.to_csv(query+'.csv', index = False)

search(query,clicks,lang)