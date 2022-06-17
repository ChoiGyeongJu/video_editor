import streamlit as st
import moviepy.editor as mp
import pafy
from utils import get_keyword, get_youtube, keyword_callback ,youtube_callback,\
                 url_callback, merge_callback, cut_video, merge_video


st.set_page_config(layout="wide")

exec(open("init.py", encoding='UTF-8'.read()))

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
</style>
""", unsafe_allow_html=True)

st.sidebar.title('EDIT HERE')
st.title('Video To Clip')

uploaded_scripts = st.file_uploader("upload scripts", type=["txt"])

if uploaded_scripts == None:
    scripts = st.text_area(label="Scripts", height=360, placeholder="스크립트를 입력하세요.")
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
            st.session_state.before_checkbox = st.session_state.url_checkbox
            st.session_state.url_checkbox = st.multiselect("CHOOSE URLS! ", st.session_state.youtube_url)  # 사용할 영상 select하는부분

for i in range(len(st.session_state.url_checkbox)):   # 영상 보여주는 부분
    set_time_title = "SET TIME " + str(i + 1) + "th VIDEO"
    col1, col2 = st.columns(2)
    url      = st.session_state.url_checkbox[i]
    best     = pafy.new(url)
    res_list = []
    for j in best.videostreams:
        res_list.append(str(j))
    video_index = res_list.index("video:webm@1280x720")
    value = best.videostreams[video_index]
    video = value.url_https
    with col1:
        st.markdown(f'<p class="video-title">{i+1}th YOUTUBE VIDEO</p>', unsafe_allow_html=True)
        st.video(url)
    
    st.sidebar.markdown(f'<p class="sidebar-title">SET TIME {i+1}th VIDEO</p>', unsafe_allow_html=True)
    start_time = st.sidebar.number_input("start time (second)", key=best.title, value=-1)
    end_time   = st.sidebar.number_input("end time (second)", key=best.videoid)
    st.sidebar.write("======================================", end='\n')
    # start_time = st.number_input("start time (second)", key=best.title, value=-1)
    # end_time   = st.number_input("end time (second)", key=best.videoid)
    if (end_time != 0) & (start_time >= 0):
        clip = cut_video(video, start_time, end_time)
        with col2:
            st.markdown('<p class="video-title">EDITED VIDEO</p>', unsafe_allow_html=True)
            st.write(clip.ipython_display(width=720, height=500))

    st.markdown('<div class="bottom-line" />', unsafe_allow_html=True)
    if st.session_state.merge_video:
        st.session_state.clip_list.append(clip)

if len(st.session_state.url_checkbox) != 0:
    if st.sidebar.button("MERGE VIDEO!!!", on_click=merge_callback):  # 구간별로 쪼갠 영상을 합치는 버튼
        print(st.session_state.clip_list)
        final_clip = merge_video(st.session_state.clip_list)
        final_clip.write_videofile("C:/Users/82102/OneDrive/바탕 화면/" + "test" + '.mp4')
        final_clip.close()
        st.success("MERGE & DOWNLOAD SUCCESS!")

        st.video("C:/Users/82102/OneDrive/바탕 화면/" + "test" + '.mp4')
