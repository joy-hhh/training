import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import time
from datetime import datetime

# ---------------------
# Google Sheets 연결 설정
# ---------------------
@st.cache_resource
def get_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    # credentials.json 대신 Streamlit Cloud의 secrets.toml 사용
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=scope
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1Ce6mcwCCe4OBpJLr1RTsCnxNB8G204bA71c-idJd6qA").sheet1
    return sheet


sheet = get_sheet()

# ---------------------
# Streamlit UI
# ---------------------
st.set_page_config(page_title="Video Training Tracker", page_icon="🎥", layout="centered")

st.title("🎥 교육 영상 시청 관리")
st.caption("이름, 등록번호, 이메일까지 입력한 다음 엔터를 누르세요.")

user = st.text_input("👤 이름 입력")
userid = st.text_input("👤 등록번호 입력")
useremail = st.text_input("👤 이메일 입력")
video_id = "training_001"

st.caption("시청시작 버튼을 누르고 Play 재생한 다음 시청종료 버튼을 누르세요.")

if user:
    st.video("https://vimeo.com/1128765663?share=copy&fl=sv&fe=ci")
    st.write("▶ 아래 버튼으로 시청 시간을 기록하세요.")

    if "start_time" not in st.session_state:
        st.session_state.start_time = None

    col1, col2 = st.columns(2)
    with col1:
        if st.button("시청 시작", type="primary"):
            st.session_state.start_time = time.time()
            st.success("시청 시작 시간을 기록했습니다.")

    with col2:
        if st.button("시청 종료", type="secondary"):
            if st.session_state.start_time:
                end_time = time.time()
                elapsed = end_time - st.session_state.start_time
                start_dt = datetime.fromtimestamp(st.session_state.start_time).strftime("%Y-%m-%d %H:%M:%S")
                end_dt = datetime.fromtimestamp(end_time).strftime("%Y-%m-%d %H:%M:%S")

                # Google Sheets에 기록
                sheet.append_row([user, userid, useremail, video_id, elapsed, start_dt, end_dt])
                st.success(f"✅ 총 {elapsed/60:.1f}분 시청 기록이 Google Sheets에 저장되었습니다.")
                st.session_state.start_time = None
            else:
                st.warning("시청 시작 버튼을 먼저 눌러주세요.")

    st.divider()
    st.info("💾 시청 로그는 시청종료 버튼 누를 때 Google Sheets에 자동 저장됩니다.")
else:
    st.info("먼저 이름, 등록번호, 이메일을 입력하세요.")
