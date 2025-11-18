import streamlit as st
from PIL import Image

st.set_page_config(page_title="AI PET CARE", layout="wide")

st.title("🐾 AI PET CARE HOME")

st.markdown("""
### 📱 반려동물 케어 AI 앱
스마트폰 홈화면처럼 구성된 UI에서 원하는 기능을 눌러 이동하세요.
""")

apps = [
    ("🐶 입양 적합성 & 품종 추천", "1_입양_적합성_및_품종_추천"),
    ("📅 건강 루틴 캘린더", "2_건강_루틴_캘린더"),
    ("❓ 증상 Q&A 안심가이드", "3_증상_QA_안심가이드"),
    ("🏥 동물병원 & 보험 비교", "4_병원_보험_비교"),
    ("💬 초보 집사 커뮤니티", "5_커뮤니티")
]

cols = st.columns(3)

for i, (label, page) in enumerate(apps):
    with cols[i % 3]:
        st.markdown(f"""
        <div style='padding: 20px; margin: 10px; border-radius:15px;
             background-color:#F2F2F2; text-align:center; font-size:20px; cursor:pointer;'>
            <a href="/{page}" target="_self" style="text-decoration:none;">{label}</a>
        </div>
        """, unsafe_allow_html=True)
