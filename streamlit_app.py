import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import base64

# K-POP 아티스트 리스트
KPOP_ARTISTS = [
    "BTS", "BLACKPINK", "NewJeans", "IVE", "LE SSERAFIM", 
    "Stray Kids", "SEVENTEEN", "EXO", "NCT", "TWICE", 
    "aespa", "ZEROBASEONE", "IU", "Taeyeon", "Jisoo", 
    "Jungkook", "V", "BIBI", "Zico"
]

# Spotify 인증 정보 (예시용 - 사용자 입력 필요)
client_id = st.secrets["SPOTIFY_CLIENT_ID"]
client_secret = st.secrets["SPOTIFY_CLIENT_SECRET"]

def get_spotify_token(client_id, client_secret):
    auth_string = f"{client_id}:{client_secret}"
    b64_auth = base64.b64encode(auth_string.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    r = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    return r.json().get("access_token")

def fetch_spotify_global_top(token):
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://api.spotify.com/v1/playlists/37i9dQZEVXbMDoHDwVN2tF"  # Top 50 Global
    r = requests.get(url, headers=headers)
    items = r.json()["tracks"]["items"]

    songs = []
    for idx, item in enumerate(items, start=1):
        name = item["track"]["name"]
        artist = ", ".join([a["name"] for a in item["track"]["artists"]])
        songs.append((idx, name, artist))

    df = pd.DataFrame(songs, columns=["순위", "곡명", "아티스트"])
    return df

# UI
st.title("🎧 Spotify Global 차트 (실시간)")
filter_kpop = st.checkbox("K-POP 아티스트만 보기", value=True)

try:
    token = get_spotify_token(client_id, client_secret)
    df = fetch_spotify_global_top(token)

    if filter_kpop:
        df = df[df["아티스트"].str.contains("|".join(KPOP_ARTISTS), case=False, na=False)]

    st.write(f"총 {len(df)}곡 표시됨")
    st.dataframe(df)

except Exception as e:
    st.error(f"Spotify 데이터를 불러오는 중 오류가 발생했습니다: {e}")