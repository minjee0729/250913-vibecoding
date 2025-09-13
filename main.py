import streamlit as st
import pandas as pd
import altair as alt
import os

st.set_page_config(page_title="MBTI 국가별 분포", layout="wide")

st.title("🌍 MBTI 유형별 비율이 가장 높은 국가 Top 10")
st.write("폴더 내 기본 데이터를 불러오되, 없을 경우 업로드한 파일을 사용합니다.")

# 기본 데이터 경로
default_path = "countriesMBTI_16types.csv"
df = None

# 1️⃣ 같은 폴더에 데이터 있는 경우 우선 사용
if os.path.exists(default_path):
    st.success(f"기본 데이터 파일 **{default_path}** 을 불러왔습니다 ✅")
    df = pd.read_csv(default_path)
else:
    # 2️⃣ 업로드한 파일 사용
    uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])
    if uploaded_file:
        st.success("업로드한 파일을 불러왔습니다 ✅")
        df = pd.read_csv(uploaded_file)

# 3️⃣ 데이터가 준비된 경우만 시각화 진행
if df is not None:
    # MBTI 유형 목록
    mbti_types = df.columns[1:].tolist()

    # 선택 박스
    selected_type = st.selectbox("🔎 MBTI 유형을 선택하세요", mbti_types)

    # 선택된 유형 기준 Top 10 국가
    top10 = df[["Country", selected_type]].nlargest(10, selected_type)

    st.subheader(f"💡 {selected_type} 유형 비율이 높은 국가 Top 10")

    # Altair 차트
    chart = (
        alt.Chart(top10)
        .mark_bar()
        .encode(
            x=alt.X(selected_type, title="비율", axis=alt.Axis(format="%")),
            y=alt.Y("Country", sort="-x", title="국가"),
            tooltip=["Country", selected_type],
            color=alt.Color("Country", legend=None)
        )
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)

    # 데이터 테이블 표시
    st.dataframe(top10.reset_index(drop=True))
else:
    st.info("CSV 파일이 필요합니다. 기본 파일이 없을 경우 업로드하세요.")
