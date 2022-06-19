import streamlit as st
from streamlit_option_menu import option_menu

import os
import moviepy.editor as mp
import pafy
import math

import uuid
import datetime

from utils import get_keyword, get_youtube, keyword_callback ,youtube_callback,\
                 url_callback, merge_callback, cut_video, merge_video, init_again


# os.environ['DISPLAY'] = ':0'
# import pyautogui

user_name = os.path.expanduser('~')
try:
    os.makedirs(f'{user_name}//Desktop//video_editor')
    os.makedirs(f'{user_name}//Desktop//video_editor//clipFiles')
    os.makedirs(f'{user_name}//Desktop//video_editor//mergedFiles')
except FileExistsError:
    pass

save_dir_clip = os.path.join(os.path.expanduser('~'), 'Desktop', 'video_editor', 'clipFiles')
save_dir_video= os.path.join(os.path.expanduser('~'), 'Desktop', 'video_editor', 'mergedFiles')

st.set_page_config(layout="wide")
exec(open("init.py", encoding='UTF-8').read())   # session state 변수 초기화

# css 부분
st.markdown("""
<style>
.sidebar-title {
    font-size: 16px;
    font-weight: 800;
    margin-borrom: 24px;
}
.video-title {
    font-size: 28px;
    font-weight: 800;
    text-align: center;
    margin-top: 30px;
}
.bottom-line {
    margin-top: 15px;
    border-bottom: 1px solid black;
}
.footer {
    margin-top: 250px;
    margin-bottom: -160px;
    color: gray;
}
</style>
""", unsafe_allow_html=True)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.sidebar.title('AIVE MENU')
st.title('VIDEO EDITOR')


if st.session_state.init_menu == True:
    uploaded_scripts = st.file_uploader("upload scripts", type=["txt"])

    if uploaded_scripts == None:
        scripts = st.text_area(label="Scripts", height=360, placeholder="TYPE OR UPLOAD SCRIPTS")
    else:
        raw_text = str(uploaded_scripts.read().lower())
        scripts_1 = raw_text.replace('\r', '')
        scripts = scripts_1.replace('\n', '')
        st.text_area(label="Scripts", height=360, value=scripts)

    keyword_list  = []
    url_info_list = []

    if (st.button("GET KEYWORD!", on_click=keyword_callback) or st.session_state.get_keyword):  # 키워드 추출 버튼
        st.write('KEYWORD LIST')
        keyword_list = get_keyword(scripts)
        st.write(keyword_list)

        if (st.button("GET YOUTUBE!", on_click=youtube_callback) or st.session_state.get_youtube):  # url 추출 버튼
            if st.session_state.youtube_url == []:
                url_info_list = get_youtube(keyword_list)
                url_callback(url_info_list)
                st.write('CLICK ABOVE BUTTON AGAIN TO ANALYZE')
                st.write(st.session_state.youtube_url)

            else:
                st.session_state.menu_title = ["HOME"]
                for i in range(len(st.session_state.youtube_url)):

                    st.session_state.clip_file.append([])
                    st.session_state.start_end.append([])
                    title = str(i + 1) + "TH VIDEO"
                    st.session_state.menu_title.append(title)   
                st.session_state.menu_title.append("MERGE HERE")
                st.session_state.init_menu = False



with st.sidebar:
    if len(st.session_state.menu_title) > 0:
        st.session_state.option_menu = option_menu("AIVE", st.session_state.menu_title, \
                            icons=['house'], menu_icon="cast")

for i in range(len(st.session_state.menu_title)):
    if st.session_state.option_menu == st.session_state.menu_title[i]:
        if i == 0:  # 새로고침해서 키워드 분석부터 다시 시작하는 부분
            st.write("IF YOU WANT TO TRY AGAIN, PLEASE REFRESH PAGE")
            # if st.button("TRY AGAIN?"):
            #     pyautogui.hotkey("ctrl", "r", "F5")

        elif i == len(st.session_state.menu_title) - 1:    # 비디오 합치는 부분
            if st.session_state.clip_file.count([]) == len(st.session_state.clip_file):
                st.write("THERE IS NO CLIP")
            else:
                st.write("VIDEO CLIP LIST")                
                video_num = 0
                cols = st.columns(3)
                for k in range(len(st.session_state.clip_file)):
                    for ik in range(len(st.session_state.clip_file[k])):
                        cols[video_num % 3].video(st.session_state.clip_file[k][ik])
                        video_num += 1
                
                if st.button("MERGE VIDEO"):
                    fileName = str(uuid.uuid1())[:8] + str(datetime.datetime.utcnow())[:10] + ".mp4"
                    
                    final_clip = []
                    for clip in st.session_state.clip_list:
                        final_clip.append(mp.VideoFileClip(clip))
                    final_video = mp.concatenate_videoclips(final_clip)
                    # final_video.write_videofile("C:/Users/82102/aive_streamlit/mergedFile/" + fileName)
                    final_video.write_videofile(os.path.join(save_dir_video, fileName))
                    st.success("MERGE FINISHED!")
                    st.video(os.path.join(save_dir_video, fileName))

        else:   # 비디오 자르고 자른것들 보는 부분
            url = st.session_state.youtube_url[i-1]
            col1, col2 = st.columns(2)
            best     = pafy.new(url)
            res_list = []
            for j in best.videostreams:
                res_list.append(str(j))
            video_index = res_list.index("video:webm@1280x720")
            value = best.videostreams[video_index]
            video = value.url_https
            with col1:
                st.markdown(f'<p class="video-title">{i}th YOUTUBE VIDEO</p>', unsafe_allow_html=True)
                st.video(url)
                st.markdown(f'<p class="sidebar-title">SET TIME {i}th VIDEO</p>', unsafe_allow_html=True)
                start_time = st.number_input("start time (second)", key=best.title, value=-1)
                end_time   = st.number_input("end time (second)", key=best.videoid)

                if st.button("CUT VIDEO"):
                    if (end_time != 0) & (start_time >= 0) & (start_time < end_time):
                        fileName = str(uuid.uuid1())
                        file_title = fileName[:8] + ".mp4"
                        clip_file_title = os.path.join(save_dir_clip, file_title)
                        clip = cut_video(video, start_time, end_time)
                        
                        st.session_state.start_end[i-1].append([start_time, end_time])
                        clip.write_videofile(clip_file_title)
                        st.session_state.clip_list.append(clip_file_title)
                        st.session_state.clip_file[i-1].append(clip_file_title)
            
            if st.session_state.clip_file[i-1] != []:
                with col2:
                    for ij in range(len(st.session_state.clip_file[i-1])):
                        section = st.session_state.start_end[i-1][ij]
                        st.markdown(f'<p class="video-title">EDITED VIDEO ({section[0]}sec ~ {math.floor(section[1])}sec)</p>', unsafe_allow_html=True)
                        st.video(st.session_state.clip_file[i-1][ij])
    

st.markdown(f'<p class="footer">email - gyeongju5142@gmail.com</p>', unsafe_allow_html=True)