import moviepy.editor as mp
import pafy
import yake
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep

def get_keyword(scripts):
    full_text = scripts
    keywords = []
    tmp = []
    kw_extractor = yake.KeywordExtractor(top=2)   # , stopwords=stop_words
    keywords = kw_extractor.extract_keywords(full_text)

    for kw, v in keywords:
        tmp.append(kw)
    keywords = tmp

    return keywords

def get_youtube(keyword_list):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    browser = webdriver.Chrome(ChromeDriverManager().install() ,options=options)

    Video_num = 2
    url_info_list       = {}   # url info list
    total_url           = []   # 스크립트 하나에 해당하는 전체 url
    url_list = []
    for i in range(len(keyword_list)):
        search_url = "https://www.youtube.com/results?search_query=" + keyword_list[i]
        browser.get(search_url)
        url_info       = []
        cnt = 1
        while len(url_info) < Video_num:    
            browser.execute_script("window.scrollTo(0, window.scrollY + 8000);")
            sleep(1)
            video_link_data = browser.find_elements(By.ID,  'video-title')
            for j in video_link_data:
                each_url_info  = {}
                if len(url_info) == Video_num:
                    break
                url = str(j.get_attribute('href'))
                if (url !='None') & (url not in total_url) & ("/shorts/" not in url):
                    video = pafy.new(url)    # KeyError: 'dislike_count' 에러시, pip install youtube-dl==2020.12.2
                    each_url_info['id'] = cnt
                    each_url_info['video_id'] = video.videoid
                    each_url_info['url'] = url
                    each_url_info['thumbnail'] = video.bigthumb
                    each_url_info['length'] = video.length
                    total_url.append(url) 
                    url_info.append(each_url_info)
                    cnt += 1

        url_info_list[str(keyword_list[i])] = url_info
    
    return total_url
    # return url_info_list