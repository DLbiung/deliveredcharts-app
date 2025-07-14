import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

def fetch_spotify_charts(region='global', date='latest'):
    url = f'https://spotifycharts.com/regional/{region}/daily/{date}'
    response = requests.get(url)
    if response.status_code != 200:
        st.error(f"Spotify 차트를 불러오는 데 실패했습니다. 상태 코드: {response.status_code}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'chart-table'})
    if not table:
        st.warning("차트 데이터가 존재하지 않습니다.")
        return pd.DataFrame()

    rows = table.find_all('tr')[1:]  # skip header
    chart_data = []
    for row in rows:
        rank = row.find('td', {'class': 'chart-table-position'}).text.strip()
        track_info = row.find('td', {'class': 'chart-table-track'})
        title = track_info.find('strong').text.strip()
        artist = track_info.find('span').text.strip().replace('by ', '')
        stream_count = row.find('td', {'class': 'chart-table-streams'}).text.strip()
        chart_data.append({
            '순위': int(rank),
            '곡 제목': title,
            '아티스트': artist,
            '스트리밍 수': stream_count
        })

    return pd.DataFrame(chart_data)

# Streamlit UI
st.title("🎧 Spotify 실시간 차트 (크롤링 기반)")
region = st.selectbox("국가 선택", ['global', 'kr'], index=0, format_func=lambda x: '🌍 글로벌' if x == 'global' else '🇰🇷 대한민국')

with st.spinner("Spotify 차트를 불러오는 중..."):
    df = fetch_spotify_charts(region)
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.error("차트 데이터를 가져오지 못했습니다.")
