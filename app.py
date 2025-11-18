import streamlit as st
import numpy as np
from datetime import datetime, timedelta
import altair as alt

# ---------------------
# 초기 세션 상태 설정
# ---------------------
if "menu" not in st.session_state:
    st.session_state.menu = "home"
if "checklist" not in st.session_state:
    st.session_state.checklist = []
if "adopt_recommended" not in st.session_state:
    st.session_state.adopt_recommended = []  # 추천 품종 보관
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

    # 입력
    col1, col2 = st.columns(2)
    with col1:
        work_hours = st.slider("근무 시간(시간/일)", 0, 12, 8)
        budget_str = st.text_input("월 예산(원)", "200000")  # 직접 입력
        try:
            budget = int(budget_str.replace(",", ""))
        except ValueError:
            budget = 0
            st.warning("예산은 숫자만 입력해 주세요.")
        noise_tolerance = st.selectbox("소음 허용도", ["낮음", "보통", "높음"])
    with col2:
        home_type = st.selectbox("주거형태", ["아파트", "단독주택", "빌라"])
        activity = st.selectbox("활동성", ["낮음", "보통", "높음"])
        allergy = st.radio("알레르기 여부", ["없음", "있음"])

    # 추천받기
    if st.button("추천 받기"):
        breeds = [
            "비글", "시바견", "골든리트리버", "푸들", "치와와", "닥스훈트", "보더콜리",
            "슈나우저", "포메라니안", "불독", "말티즈", "래브라도", "요크셔테리어",
            "시추", "말라뮤트", "웰시코기", "보스턴테리어", "닥스훈트(장모)", "시바견(소형)",
            "진돗개", "기타"
        ]
        recommended = list(np.random.choice(breeds, 3, replace=False))
        st.session_state.adopt_recommended = recommended

    # 추천 결과가 있을 때만 보이게
    if st.session_state.adopt_recommended:
        st.subheader("추천 품종")
        for idx, breed in enumerate(st.session_state.adopt_recommended, 1):
            st.write(f"{idx}. {breed}")

        # 체크리스트
        checklist_items = ["사료", "배변패드", "목줄/하네스", "장난감", "목욕용품", "건강검진 예약"]
        st.subheader("필수 준비물 체크리스트")
        for item in checklist_items:
            # 체크박스 기본값을 기존 세션 상태로
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

    breeds = [
        "비글", "시바견", "골든리트리버", "푸들", "치와와", "닥스훈트", "보더콜리",
        "슈나우저", "포메라니안", "불독", "말티즈", "래브라도", "요크셔테리어",
        "시추", "말라뮤트", "웰시코기", "보스턴테리어", "닥스훈트(장모)", "시바견(소형)",
        "진돗개", "기타"
    ]
    selected_breed = st.selectbox("강아지 품종 선택", breeds)
    age_months = st.number_input("나이(개월)", 0, 240, 6)

    # 품종을 선택했으면 스케줄 보여줌
    if selected_breed:
        st.subheader("권장 예방접종 스케줄")
        today = datetime.today()
        vaccines = ["종합백신", "광견병", "코로나", "심장사상충"]
        for i, vac in enumerate(vaccines):
            st.write(f"{vac}: {(today + timedelta(days=i * 30)).strftime('%Y-%m-%d')}")

    st.subheader("건강 루틴 기록")

    # 체중 기록 (그래프용 데이터)
    if "weights" not in st.session_state:
        st.session_state.weights = []  # (날짜, 체중) 쌍 저장

    weight = st.number_input("체중(kg)", 0.0, 100.0, 5.0)
    if st.button("체중 저장"):
        st.session_state.weights.append((datetime.today(), weight))

    # 체중 그래프
    if st.session_state.weights:
        df = {
            "date": [w[0] for w in st.session_state.weights],
            "weight": [w[1] for w in st.session_state.weights]
        }
        chart = alt.Chart(
            alt.Data(values=[{"date": d.isoformat(), "weight": wt} for d, wt in zip(df["date"], df["weight"])])
        ).mark_line(point=True).encode(
            x=alt.X("date:T", title="날짜"),
            y=alt.Y("weight:Q", title="체중 (kg)")
        )
        st.altair_chart(chart, use_container_width=True)

    poop = st.selectbox("배변 패턴", ["정상", "변비", "설사"])
    if poop != "정상":
        st.warning("루틴 이탈 감지: 이상 패턴!")

    st.button("🏠 홈으로", on_click=go_home, key="home_back2")

# ---------------------
# 3. 증상 Q&A
# ---------------------
def qa_screen():
    st.header("❓ 증상 Q&A ‘안심 가이드’")

    symptom = st.text_input("증상 입력 (예: 구토, 설사 등)")

    if st.button("검색"):
        # 간단 예시 해결 로직
        advice = []
        lower = symptom.lower()
        if "구토" in lower:
            advice.append("구토가 하루 이상 지속되면 즉시 동물병원에 가는 것이 좋습니다.")
        if "설사" in lower:
            advice.append("설사가 계속되면 탈수 위험이 있으므로 수분을 자주 공급하고 필요시 진료를 고려하세요.")
        if "식욕" in lower or "먹" in lower:
            advice.append("식욕이 많이 떨어지면 건강 상태를 체크할 필요가 있습니다.")
        if "호흡" in lower:
            advice.append("호흡이 빠르거나 곤란하면 응급 상태일 수 있으니 즉시 병원 방문을 권장합니다.")
        if not advice:
            advice.append("증상 정보가 제한적입니다. 가능한 빨리 수의사 상담을 추천드립니다.")

        st.subheader("🔍 해결 가이드")
        for a in advice:
            st.write("• " + a)

    st.button("🏠 홈으로", on_click=go_home, key="home_back3")

# ---------------------
# 4. 병원 & 보험 비교
# ---------------------
def compare_screen():
    st.header("🏥 병원 & 보험 비교")

    # 병원 검색 (지역 기반)
    st.subheader("병원 검색")
    region = st.text_input("지역 입력 (예: 서울, 부산 등)")
    if st.button("검색 병원", key="hospital_search"):
        # 예시 병원 데이터 (실제 데이터 사용하는 것이 어려울 수 있어서 더미 + 설명)
        # 실제 앱이라면 공공 DB + API 필요
        sample_hospitals = [
            {"name": "서울24시동물병원", "location": "서울", "special": "24시"},
            {"name": "부산펫케어", "location": "부산", "special": "내과 / 외과"}
        ]
        hits = [h for h in sample_hospitals if region in h["location"]]
        if hits:
            for h in hits:
                st.write(f"- {h['name']} ({h['location']}) — 전문: {h['special']}")
        else:
            st.info("해당 지역에 등록된 병원이 없습니다.")

    # 보험 비교 (실제 펫보험 데이터 일부 반영)
    st.subheader("펫보험 비교")
    # 아이펫 애니펫의 보험 보장 범위 일부 예시 (아이펫 사이트 참고) :contentReference[oaicite:0]{index=0}
    insurance_products = [
        {
            "회사": "삼성화재 (애니펫)",
            "보장 범위": "치료비 70% (질병/상해)",
            "특약 / 주의": "수술 연 2회 제한, 1회 최대 청구 한도 존재",
            "가입 가능 연령": "생후 약 2개월 ~ 8세"  # 아이펫 정보 기반 :contentReference[oaicite:1]{index=1}
        },
        {
            "회사": "DB손해보험 펫보험 (예시)",
            "보장 범위": "입원 + 외래 치료 보장 특화",
            "특약": "특정 수술 특약 가능",
            "가입 가능 연령": "견 / 묘에 따라 다름"
        }
        # 실제 보험 정보를 더 채워야 함(공시자료, 약관 등 참조 필요)
    ]
    for ins in insurance_products:
        st.write(f"**{ins['회사']}**")
        st.write(f"- 보장 범위: {ins['보장 범위']}")
        st.write(f"- 특약 / 주의: {ins.get('특약', '-')}")
        st.write(f"- 가입 가능 연령: {ins.get('가입 가능 연령', '-')}")
        st.write("---")

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
            st.session_state.posts.append({"text": user_post, "likes": 0, "comments": []})

    # 게시글 + 댓글
    for i, post in enumerate(st.session_state.posts):
        st.write(f"게시글 {i+1}: {post['text']}")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(f"❤️ 좋아요 {i}", key=f"like_{i}"):
                post["likes"] += 1
        with col2:
            with st.form(f"comment_form_{i}"):
                comment_text = st.text_input("댓글 작성", key=f"comment_input_{i}")
                comment_submitted = st.form_submit_button("댓글 등록", key=f"comment_btn_{i}")
                if comment_submitted and comment_text:
                    post["comments"].append(comment_text)

        # 댓글 표시
        if post["comments"]:
            st.subheader("🗨 댓글")
            for c_idx, comment in enumerate(post["comments"], 1):
                st.write(f"{c_idx}. {comment}")

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

