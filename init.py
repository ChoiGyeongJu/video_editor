import streamlit as st
import moviepy.editor as mp


if "init_menu"       not in st.session_state: st.session_state.init_menu       = True
if "option_menu"     not in st.session_state: st.session_state.option_menu     = []
if "menu_title"      not in st.session_state: st.session_state.menu_title      = []
if "keyword_num"     not in st.session_state: st.session_state.keyword_num     = 0
if "each_url_num"     not in st.session_state: st.session_state.each_url_num     = 0
if "start_end"       not in st.session_state: st.session_state.start_end       = []
if "init_menu"       not in st.session_state: st.session_state.init_menu       = True
if "option_menu"     not in st.session_state: st.session_state.option_menu     = []
if "menu_title"      not in st.session_state: st.session_state.menu_title      = []
if "get_keyword"     not in st.session_state: st.session_state.get_keyword     = False
if "get_youtube"     not in st.session_state: st.session_state.get_youtube     = False
if "youtube_url"     not in st.session_state: st.session_state.youtube_url     = []
if "start_time"      not in st.session_state: st.session_state.start_time      = []
if "end_time"        not in st.session_state: st.session_state.end_time        = []
if "before_checkbox" not in st.session_state: st.session_state.before_checkbox = []
if "url_checkbox"    not in st.session_state: st.session_state.url_checkbox    = []
if "clip_list"       not in st.session_state: st.session_state.clip_list       = []
if "merge_video"     not in st.session_state: st.session_state.merge_video     = False

if "clip_file" not in st.session_state: st.session_state.clip_file = []
    
