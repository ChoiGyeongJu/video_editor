import streamlit as st
import moviepy.editor as mp
import pafy
from utils import get_keyword, get_youtube

#  session 변수 초기화
if "get_keyword" not in st.session_state:
    st.session_state.get_keyword = False

if "get_youtube" not in st.session_state:
    st.session_state.get_youtube = False

if "youtube_url" not in st.session_state:
    st.session_state.youtube_url = []

if "url_checkbox" not in st.session_state:
    st.session_state.url_checkbox = []

if "clip_list" not in st.session_state:
    st.session_state.clip_list = []

if "merge_video" not in st.session_state:
    st.session_state.merge_video = False
    
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


st.title('Video To Clip')

uploaded_scripts = st.file_uploader("upload scripts", type=["txt"])

if uploaded_scripts == None:
    scripts = st.text_area(label="Scripts", height=200, placeholder="스크립트를 입력하세요.")
else:
    raw_text = str(uploaded_scripts.read().lower())
    scripts_1 = raw_text.replace('\r', '')
    scripts = scripts_1.replace('\n', '')
    st.text_area(label="Scripts", height=200, value=scripts)

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
            st.session_state.url_checkbox = st.multiselect("CHOOSE URLS! ", st.session_state.youtube_url)  # 사용할 영상 select하는부분
            
            for i in range(len(st.session_state.url_checkbox)):
                url      = st.session_state.url_checkbox[i]
                best     = pafy.new(url)
                res_list = []
                for i in best.videostreams:
                    res_list.append(str(i))
                video_index = res_list.index("video:webm@1280x720")
                value = best.videostreams[video_index]
                video = value.url_https
                st.video(url)
                start_time = st.number_input("start time (second)", key=best.title)
                end_time = st.number_input("end time (second)", min_value=1,key=best.videoid)
                clip = cut_video(video, start_time, end_time)
                st.write(clip.ipython_display(width=680))

                if st.session_state.merge_video:
                    st.session_state.clip_list.append(clip)

            if st.button("MERGE VIDEO!!!", on_click=merge_callback):  # 구간별로 쪼갠 영상을 합치는 버튼
                print(st.session_state.clip_list)
                final_clip = merge_video(st.session_state.clip_list)
                final_clip.write_videofile("C:/Users/82102/OneDrive/바탕 화면/" + "test" + '.mp4')
                final_clip.close()
                st.success("MERGE & DOWNLOAD SUCCESS!")

                st.video("C:/Users/82102/OneDrive/바탕 화면/" + "test" + '.mp4')

               
# st.write("로컬 영상 사용")
# uploaded_video = st.file_uploader("Upload mp4 file",type=["mp4","mpeg"])
# if uploaded_video is not None:
#     st.video(uploaded_video)

#     fileName = uploaded_video.name  # 파일 이름
#     with open(fileName, mode='wb') as f:
#         f.write(uploaded_video.read()) 
#     st_video = open(fileName,'rb')      
#     clip = cut_video(fileName)

#     if st.button("Download"):
#         clip.write_videofile("C:/Users/82102/OneDrive/바탕 화면/clip_" + fileName)
#         clip.close()
#         st.success("Download Success!")

#         st.video("C:/Users/82102/OneDrive/바탕 화면/clip_" + fileName)
