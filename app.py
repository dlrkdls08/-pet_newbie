import streamlit as st
import numpy as np
from datetime import datetime, timedelta

# ---------------------
# 초기 세션 상태 설정
# ---------------------
if "menu" not in st.session_state:
    st.session_state.menu = "home"
if "checklist" not in st.session_state:
    st.session_state.checklist = []
if "posts" not in st.session_state:
    st.session_state.posts = []

def go_home():
    st.session_state.menu = "home"

# ---------------------
# 홈 화면
# ---------------------
def home_screen():
    st.title("🐾 Pet Newbie AI App")
    st.write("원하는 기능을 선택하세요:")

    cols = st.columns(3)
    home_buttons = [
        ("🐶 입양 & 품종 추천", "adopt"),
        ("📅 건강 루틴 캘린더", "calendar"),
        ("❓ 증상 Q&A", "qa"),
        ("🏥 병원 & 보험 비교", "compare"),
        ("💬 커뮤니티", "community"),
    ]

    for i, (label, key) in enumerate(home_buttons):
        with cols[i % 3]:
            if st.button(label, key=f"home_btn_{i}"):
                st.session_state.menu = key

# ---------------------
# 1. 입양 적합성 & 품종 추천
# ---------------------
def adopt_screen():
    st.header("🐶 입양 적합성 & 품종 추천")

    col1, col2 = st.columns(2)
    with col1:
        work_hours = st.slider("근무 시간(시간/일)", 0, 12, 8)
        budget_str = st.text_input("월 예산(원)", "200000")  # 직접 입력 가능
        try:
            budget = int(budget_str.replace(",", ""))
        except ValueError:
            budget = 0
            st.warning("숫자만 입력하세요")
        noise_tolerance = st.selectbox("소음 허용도", ["낮음", "보통", "높음"])
    with col2:
        home_type = st.selectbox("주거형태", ["아파트", "단독주택", "빌라"])
        activity = st.selectbox("활동성", ["낮음", "보통", "높음"])
        allergy = st.radio("알레르기 여부", ["없음", "있음"])

    if st.button("추천 받기"):
        breeds = ["비글","시바견","골든리트리버","푸들","치와와","닥스훈트","보더콜리","슈나우저",
                  "포메라니안","불독","말티즈","래브라도","요크셔테리어","시추","말라뮤트","웰시코기",
                  "보스턴테리어","닥스훈트(장모)","시바견(소형)","진돗개","기타"]
        recommended = np.random.choice(breeds, 3, replace=False)
        st.subheader("추천 품종")
        for idx, breed in enumerate(recommended, 1):
            st.write(f"{idx}. {breed}")

        checklist_items = ["사료", "배변패드", "목줄/하네스", "장난감", "목욕용품", "건강검진 예약"]
        st.subheader("필수 준비물 체크리스트")
        for item in checklist_items:
            checked = st.checkbox(item, key=f"check_{item}", value=(item in st.session_state.checklist))
            if checked and item not in st.session_state.checklist:
                st.session_state.checklist.append(item)
            elif not checked and item in st.session_state.checklist:
                st.session_state.checklist.remove(item)
        st.write("✅ 선택 완료:", st.session_state.checklist)

    st.button("🏠 홈으로", on_click=go_home, key="home_back1")

# ---------------------
# 2. 예방접종 & 건강 루틴
# ---------------------
def calendar_screen():
    st.header("📅 예방접종 & 건강 루틴")

    breeds = ["비글","시바견","골든리트리버","푸들","치와와","닥스훈트","보더콜리","슈나우저",
              "포메라니안","불독","말티즈","래브라도","요크셔테리어","시추","말라뮤트","웰시코기",
              "보스턴테리어","닥스훈트(장모)","시바견(소형)","진돗개","기타"]
    selected_breed = st.selectbox("강아지 품종 선택", breeds)
    age_months = st.number_input("나이(개월)", 0, 240, 6)

    if selected_breed:
        st.subheader("권장 예방접종 스케줄")
        today = datetime.today()
        vaccines = ["종합백신", "광견병", "코로나", "심장사상충"]
        for i, vac in enumerate(vaccines):
            st.write(f"{vac}: {(today + timedelta(days=i*30)).strftime('%Y-%m-%d')}")

    st.subheader("건강 루틴 기록")
    weight = st.number_input("체중(kg)", 0.0, 100.0, 5.0)
    poop = st.selectbox("배변 패턴", ["정상", "변비", "설사"])
    if poop != "정상":
        st.warning("루틴 이탈 감지: 이상 패턴!")

    st.button("🏠 홈으로", on_click=go_home, key="home_back2")

# ---------------------
# 3. 증상 Q&A
# ---------------------
def qa_screen():
    st.header("❓ 증상 Q&A ‘안심 가이드’")
    symptom = st.text_input("증상 입력")
    if st.button("검색"):
        st.write("⚠️ 자가처치 금지 / 위험 신호 / 즉시 내원 기준 안내")

    st.button("🏠 홈으로", on_click=go_home, key="home_back3")

# ---------------------
# 4. 병원 & 보험 비교
# ---------------------
def compare_screen():
    st.header("🏥 병원 & 보험 비교")

    st.subheader("병원 검색")
    region = st.text_input("지역 입력")
    if st.button("검색", key="hospital_search"):
        st.write(f"{region} 근처 병원 검색 결과 (예시)")

    st.subheader("보험 비교 (예시 실제 데이터 기반)")
    insurance_data = [
        {"name":"A보험","보장범위":"질병/상해","자기부담률":"10%","특약":"소형견 고빈도 질환"},
        {"name":"B보험","보장범위":"질병/상해","자기부담률":"15%","특약":"반려묘 심장/신장 특약"},
        {"name":"C보험","보장범위":"질병/상해","자기부담률":"12%","특약":"중대 질병 특약"}
    ]
    for ins in insurance_data:
        st.write(ins)

    st.button("🏠 홈으로", on_click=go_home, key="home_back4")

# ---------------------
# 5. 커뮤니티
# ---------------------
def community_screen():
    st.header("💬 커뮤니티")
    with st.form("post_form"):
        user_post = st.text_area("게시글 작성")
        submitted = st.form_submit_button("게시글 올리기")
        if submitted and user_post:
            st.session_state.posts.append({"text": user_post, "likes": 0, "comments":[]})

    for i, post in enumerate(st.session_state.posts):
        st.write(f"게시글 {i+1}: {post['text']}")
        col1, col2 = st.columns([1,1])
        with col1:
            if st.button(f"❤️ 좋아요 {i}", key=f"like_{i}"):
                post["likes"] += 1
        with col2:
            with st.form(f"comment_form_{i}"):
                comment_text = st.text_input("댓글 작성", key=f"comment_input_{i}")
                comment_submitted = st.form_submit_button("댓글 등록", key=f"comment_btn_{i}")
                if comment_submitted and comment_text:
                    post["comments"].append(comment_text)

        if post["comments"]:
            for c_idx, comment in enumerate(post["comments"], 1):
                st.write(f"> 댓글 {c_idx}: {comment}")

    st.button("🏠 홈으로", on_click=go_home, key="home_back5")

# ---------------------
# 메뉴 전환
# ---------------------
menu_dict = {
    "home": home_screen,
    "adopt": adopt_screen,
    "calendar": calendar_screen,
    "qa": qa_screen,
    "compare": compare_screen,
    "community": community_screen
}

menu_dict.get(st.session_state.menu, home_screen)()
