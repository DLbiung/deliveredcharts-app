import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# K-POP 아티스트 리스트
KPOP_ARTISTS = [
    "BTS", "BLACKPINK", "NewJeans", "IVE", "LE SSERAFIM", 
    "Stray Kids", "SEVENTEEN", "EXO", "NCT", "TWICE", 
    "aespa", "ZEROBASEONE", "IU", "Taeyeon", "Jisoo", 
    "Jungkook", "V", "BIBI", "Zico"
]

# 차트 옵션
chart_option = st.selectbox("차트를 선택하세요", ["Spotify Global", "Billboard Global 200", "Billboard Hot 100", "Billboard Global Excl. US"])
filter_kpop = st.checkbox("K-POP 아티스트만 보기", value=True)

# Billboard 크롤링 함수
def fetch_billboard_chart(chart_name):
    chart_urls = {
        "Billboard Global 200": "https://www.billboard.com/charts/billboard-global-200/",
        "Billboard Hot 100": "https://www.billboard.com/charts/hot-100/",
        "Billboard Global Excl. US": "https://www.billboard.com/charts/billboard-global-excl-us/"
    }
    url = chart_urls[chart_name]
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")

    titles = [t.get_text(strip=True) for t in soup.select("li.o-chart-results-list__item h3")]
    artists = [a.get_text(strip=True) for a in soup.select("li.o-chart-results-list__item span.c-label") if a.get("class") == ['c-label']]

    min_len = min(len(titles), len(artists))
    chart_data = pd.DataFrame({
        "순위": range(1, min_len + 1),
        "곡명": titles[:min_len],
        "아티스트": artists[:min_len]
    })
    return chart_data

# Spotify 예시 (실제 API 연동 시 변경 필요)
def fetch_spotify_chart():
    return pd.DataFrame({
        "순위": list(range(1, 11)),
        "곡명": ["Seven", "ETA", "Super Shy", "I AM", "ANTIFRAGILE", "Hype Boy", "Butter", "Shut Down", "Love Dive", "Next Level"],
        "아티스트": ["Jungkook", "NewJeans", "NewJeans", "IVE", "LE SSERAFIM", "NewJeans", "BTS", "BLACKPINK", "IVE", "aespa"]
    })

# 차트 가져오기
if chart_option == "Spotify Global":
    df = fetch_spotify_chart()
else:
    df = fetch_billboard_chart(chart_option)

# K-POP 필터 적용
if filter_kpop:
    df = df[df["아티스트"].str.contains('|'.join(KPOP_ARTISTS), case=False, na=False)]

st.title(f"{chart_option} 차트")
st.write(f"총 {len(df)}곡 표시됨")
st.dataframe(df)