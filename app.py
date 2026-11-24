
# ===== 설정 =====
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Titanic 대시보드", layout="wide")


# ===== 함수 =====
def filter_data(df, sexes, classes, age_range):
    f = df[df["sex"].isin(sexes)
           & df["pclass"].isin(classes)]
    # 나이 범위가 전체(0~80)가 아닐 때만 나이 조건 적용 (나이 결측 승객 유지)
    if age_range != (0, 80):
        f = f[f["age"].between(*age_range)]
    return f

def kpi(df):
    if len(df) == 0:
        return 0, 0, 0
    n = len(df)
    rate = round(df["survived"].mean() * 100, 1)
    age = round(df["age"].mean(), 1)
    return n, rate, age

def class_rate_bar(df):
    r = (df.groupby("pclass")["survived"]
           .mean().mul(100).round(1)
           .reset_index())
    r["pclass"] = r["pclass"].astype(str) + "등급"
    return px.bar(r, x="pclass", y="survived", text="survived",
                  title="객실 등급별 생존율(%)")

def age_hist(df):
    return px.histogram(df, x="age", color="survived", barmode="overlay",
                        opacity=0.6, title="생존 여부별 나이 분포")


# ===== 데이터 읽기 =====
@st.cache_data
def load_data():
    return pd.read_csv("titanic.csv")
df = load_data()


# ===== 제목 =====
st.title("타이타닉, 누가 살아남았나?")


# ===== 사이드바 =====
sexes = st.sidebar.multiselect("성별", ["male", "female"], ["male", "female"])
classes = st.sidebar.multiselect("객실 등급", [1, 2, 3], [1, 2, 3])
ages = st.sidebar.slider("나이", 0, 80, (0, 80))

if not sexes or not classes:
    st.warning("성별과 등급을 하나 이상 선택하세요.")
    st.stop()


# ===== 필터 =====
f = filter_data(df, sexes, classes, ages)

if len(f) == 0:
    st.warning("조건에 맞는 승객이 없습니다.")
    st.stop()


# ===== KPI =====
n, rate, age = kpi(f)
c1, c2, c3 = st.columns(3)
c1.metric("승객 수", f"{n}명")
c2.metric("생존율", f"{rate}%")
c3.metric("평균 나이", f"{age}세")


# ===== 차트 · 표 =====
left, right = st.columns(2)
left.plotly_chart(class_rate_bar(f))
right.plotly_chart(age_hist(f))

with st.expander("데이터 보기"):
    st.dataframe(f)
