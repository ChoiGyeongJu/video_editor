import moviepy.editor as mp
import pafy
import yake
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep
import streamlit as st

def get_keyword(scripts, n):
    full_text = scripts
    keywords = []
    tmp = []
    kw_extractor = yake.KeywordExtractor(top=n)   # , stopwords=stop_words
    keywords = kw_extractor.extract_keywords(full_text)

    for kw, v in keywords:
        tmp.append(kw)
    keywords = tmp

    return keywords

def get_youtube(keyword_list, n):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    
    Video_num = n
    total_url           = []   # 스크립트 하나에 해당하는 전체 url

    for i in range(len(keyword_list)):
        search_url = "https://www.youtube.com/results?search_query=" + keyword_list[i]
        browser.get(search_url)

        while len(total_url) < Video_num:    
            browser.execute_script("window.scrollTo(0, window.scrollY + 8000);")
            sleep(1)
            video_link_data = browser.find_elements(By.ID,  'video-title')
            for j in video_link_data:
                if len(total_url) == Video_num:
                    break
                url = str(j.get_attribute('href'))
                if (url !='None') & (url not in total_url) & ("/shorts/" not in url):
                    total_url.append(url) 

    return total_url
    # return url_info_list

def keyword_callback():
    st.session_state.get_keyword = True

def youtube_callback():
    st.session_state.get_youtube = True

def url_callback(url_list):
    st.session_state.youtube_url = url_list

def merge_callback():
    st.session_state.merge_video = True

def cut_video(video, start, end):
    clip = mp.VideoFileClip(video).subclip(start, end)
    return clip

def merge_video(clip_list):
    final_clip = mp.concatenate_videoclips(clip_list)
    return final_clip

def init_again():
    st.session_state.option_menu     = []
    st.session_state.menu_title      = []
    st.session_state.edited_clip     = []
    st.session_state.start_end       = []
    st.session_state.end_time        = []
    st.session_state.before_checkbox = []
    st.session_state.url_checkbox    = []
    st.session_state.clip_list       = []
    st.session_state.merge_video     = False
    st.session_state.get_keyword     = False
    st.session_state.get_youtube     = False
    st.session_state.youtube_url     = []
    st.session_state.init_menu       = True   
         
