# pages/1_입양_적합성_및_품종_추천.py
import streamlit as st
import pickle
import numpy as np
from models.rule_based_breed_selector import rule_based_filter

st.title("🐶 입양 적합성 & 품종 추천")

st.markdown("AI 온보딩 기반 맞춤 품종 추천")

# ------------------------------
# 사용자 입력
# ------------------------------
work = st.selectbox("근무 시간", ["짧음", "보통", "김"])
house = st.selectbox("주거 형태", ["원룸", "아파트", "주택"])
activity = st.selectbox("활동성", ["낮음", "보통", "높음"])
budget = st.slider("월 예상 예산", 10, 200, 50)
allergy = st.selectbox("알레르기 여부", ["없음", "약함", "심함"])
noise = st.selectbox("소음 허용도", ["낮음", "보통", "높음"])

if st.button("AI 품종 추천 받기"):
    # 규칙 기반 필터링
    rule_candidates = rule_based_filter(work, house, activity, budget, allergy, noise)

    st.subheader("📌 1단계: 규칙 기반 필터링 결과")
    st.write(rule_candidates)

    # Gradient Boosting 모델 불러오기
    with open("models/gbm_breed_model.pkl", "rb") as f:
        model = pickle.load(f)

    # 특징 벡터 생성
    x = np.array([[len(work), len(house), len(activity), budget]])

    gbm_score = model.predict(x)[0]

    st.subheader("📌 2단계: ML 기반 품종 적합도 예측")
    st.write("예측 점수:", gbm_score)

    # 최종 추천
    final = sorted(rule_candidates, key=lambda x: abs(len(x) - gbm_score))
    best = final[:3]

    st.success("✨ 최종 추천 품종")
    st.write(best)

    # 자동 생성 정보
    st.subheader("📦 자동 준비물 체크리스트")
    st.write(["사료", "배변패드", "리드줄", "장난감", "하우스"])

    st.subheader("📊 월 예상비")
    st.write(f"{budget}만원 ± 20%")

    st.subheader("📘 초보 난이도")
    st.write("중간")
