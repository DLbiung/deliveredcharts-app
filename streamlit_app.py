
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 차트 옵션
chart_option = st.selectbox("차트를 선택하세요", ["Spotify Global", "Billboard Global 200", "Billboard Hot 100", "Billboard Global Excl. US"])

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

    chart_data = pd.DataFrame({
        "순위": range(1, len(titles) + 1),
        "곡명": titles[:len(artists)],
        "아티스트": artists[:len(titles)]
    })
    return chart_data

# Spotify API 예시 함수 (실제 API 연동 시 업데이트 필요)
def fetch_spotify_chart():
    return pd.DataFrame({
        "순위": [1, 2, 3],
        "곡명": ["Example Song A", "Example Song B", "Example Song C"],
        "아티스트": ["Artist A", "Artist B", "Artist C"]
    })

# 차트 데이터 불러오기
if chart_option == "Spotify Global":
    df = fetch_spotify_chart()
else:
    df = fetch_billboard_chart(chart_option)

st.title(f"{chart_option} 차트")
st.dataframe(df)
