import streamlit as st
import json
import numpy as np
import pickle

# ---------------------------------------------------------
# 기본 설정
# ---------------------------------------------------------
st.set_page_config(page_title="AI PET CARE", layout="wide")
st.title("🐾 반려동물 AI 케어 앱")

st.markdown("### 아래에서 기능을 선택하세요!")

menu = st.sidebar.radio(
    "메뉴 선택",
    [
        "📱 홈",
        "🐶 입양 적합성 & 품종 추천",
        "📅 건강 루틴 캘린더",
        "❓ 증상 Q&A 안심가이드 (RAG)",
        "🏥 병원 & 보험 비교",
        "💬 커뮤니티"
    ]
)

# ---------------------------------------------------------
# 내부 데이터 (JSON 파일 없이 코드에 포함)
# ---------------------------------------------------------

vaccination_data = {
    "강아지": {
        "2": {"백신": "종합백신 1차", "설명": "기초접종 시작"},
        "3": {"백신": "종합백신 2차", "설명": "면역 강화"},
        "4": {"백신": "종합백신 3차 + 코로나", "설명": "추가 예방"},
        "12": {"백신": "광견병", "설명": "1년에 한번 접종"}
    },
    "고양이": {
        "2": {"백신": "종합백신 1차", "설명": "기초접종 시작"},
        "3": {"백신": "종합백신 2차", "설명": "면역 강화"},
        "4": {"백신": "종합백신 3차", "설명": "완료"}
    }
}

hospital_list = [
    {"name": "서울24시동물병원", "location": "서울", "special": "24시"},
    {"name": "해밀동물메디컬센터", "location": "부산", "special": "내과"},
    {"name": "수원동물병원", "location": "수원", "special": "외과"}
]

insurance_plans = [
    {"회사": "A보험", "보장": "기본 진료 + 입원", "자기부담": "20%"},
    {"회사": "B보험", "보장": "입원 + 수술", "자기부담": "30%"},
    {"회사": "C보험", "보장": "수술 특화", "자기부담": "10%"}
]

# 가상 RAG 문서
rag_docs = [
    "구토가 하루 이상 지속되면 즉시 병원 방문이 필요합니다.",
    "혈변은 응급 신호로 분류되며 빠른 검사 권장.",
    "식욕 부진이 24시간 이상 지속되면 진료를 받아야 합니다.",
    "호흡 곤란은 지체 없는 내원이 필요합니다."
]

# 커뮤니티 데이터 저장 메모리 (파일 저장 없이 동작)
if "community" not in st.session_state:
    st.session_state.community = []

# ---------------------------------------------------------
# 기능 ① 입양 적합성 & 품종 추천
# ---------------------------------------------------------
if menu == "🐶 입양 적합성 & 품종 추천":
    st.header("🐶 입양 적합성 & 품종 추천")

    work = st.selectbox("근무 시간", ["짧음", "보통", "김"])
    house = st.selectbox("주거 형태", ["원룸", "아파트", "주택"])
    activity = st.selectbox("활동성", ["낮음", "보통", "높음"])
    budget = st.slider("월 예상 예산(만원)", 10, 200, 50)
    allergy = st.selectbox("알레르기 여부", ["없음", "약함", "심함"])
    noise = st.selectbox("소음 허용도", ["낮음", "보통", "높음"])

    if st.button("추천 받기"):
        breeds = ["푸들", "말티즈", "시바견", "러시안블루", "코숏"]

        # 규칙 기반 필터
        filtered = []
        for b in breeds:
            if allergy == "심함" and b not in ["푸들", "러시안블루"]:
                continue
            if budget < 20 and b == "시바견":
                continue
            filtered.append(b)

        st.subheader("📌 규칙 기반 추천 품종")
        st.write(filtered)

        # 간이 ML (예시): 문자열 길이 기반 더미 모델
        score = abs(len(work) + len(house) + len(activity) - budget % 10)

        sorted_breeds = sorted(filtered, key=lambda x: abs(len(x) - score))
        best = sorted_breeds[:3]

        st.success("✨ 최종 추천")
        st.write(best)

        st.subheader("📦 기본 준비물 체크리스트")
        st.write(["사료", "배변패드", "리드줄", "장난감"])

        st.subheader("📊 월 예상비")
        st.write(f"{budget}만원 (±20%)")

# ---------------------------------------------------------
# 기능 ② 건강 루틴 캘린더
# ---------------------------------------------------------
elif menu == "📅 건강 루틴 캘린더":
    st.header("📅 건강 루틴 캘린더")

    species = st.selectbox("종", ["강아지", "고양이"])
    age = st.number_input("나이(개월)", 1, 240)

    if st.button("스케줄 보기"):
        age_str = str(age)
        if age_str in vaccination_data[species]:
            st.json(vaccination_data[species][age_str])
        else:
            st.info("해당 나이에 대한 접종 정보가 없습니다.")

    st.subheader("📈 체중/배변 이상치 탐지")
    weight = st.number_input("체중(kg)", 0.1, 100.0)
    poop = st.selectbox("배변 상태", ["정상", "무름", "딱딱함", "혈변"])

    if st.button("상태 분석"):
        if poop == "혈변":
            st.error("🚨 응급 신호: 즉시 병원 방문 필요")
        elif weight < 1:
            st.warning("체중이 낮습니다. 주의하세요.")
        else:
            st.success("정상 범위로 보입니다.")

# ---------------------------------------------------------
# 기능 ③ 증상 Q&A (RAG)
# ---------------------------------------------------------
elif menu == "❓ 증상 Q&A 안심가이드 (RAG)":
    st.header("❓ 증상 Q&A — 안심가이드")

    q = st.text_input("증상을 입력하세요")

    if st.button("검색"):
        st.warning("⚠️ 이 도구는 의학적 진단을 제공하지 않습니다.")
        st.write("수의사 감수 문서 기반 RAG 결과:")

        results = []
        for doc in rag_docs:
            if any(word in doc for word in q.split()):
                results.append(doc)

        if not results:
            results = rag_docs[:2]

        for r in results:
            st.write("- ", r)

# ---------------------------------------------------------
# 기능 ④ 병원 & 보험 비교
# ---------------------------------------------------------
elif menu == "🏥 병원 & 보험 비교":
    st.header("🏥 동물병원 & 보험 비교")

    st.subheader("📌 병원 검색")
    keyword = st.text_input("병원명/지역 검색")

    if st.button("검색"):
        hits = [h for h in hospital_list if keyword in h["name"] or keyword in h["location"]]
        st.write(hits)

    st.subheader("📌 보험 비교")
    st.table(insurance_plans)

# ---------------------------------------------------------
# 기능 ⑤ 커뮤니티
# ---------------------------------------------------------
elif menu == "💬 커뮤니티":
    st.header("💬 초보 집사 커뮤니티")

    st.subheader("✏️ 글쓰기")
    author = st.text_input("작성자")
    content = st.text_area("내용")

    if st.button("게시"):
        st.session_state.community.append(
            {"author": author, "content": content, "likes": 0, "comments": []}
        )
        st.success("게시 완료!")

    st.subheader("📌 게시판")
    for idx, p in enumerate(st.session_state.community):
        st.markdown(f"### {p['author']}")
        st.write(p["content"])
        st.write(f"♥ {p['likes']}")

        if st.button(f"좋아요_{idx}"):
            p["likes"] += 1
            st.experimental_rerun()

        st.write("💬 댓글:")
        for c in p["comments"]:
            st.write(f" - {c}")

        comment = st.text_input(f"댓글 입력 {idx}")
        if st.button(f"댓글 등록 {idx}"):
            p["comments"].append(comment)
            st.experimental_rerun()
