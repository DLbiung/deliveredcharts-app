import streamlit as st
import requests
import pandas as pd
import base64

# K-POP 아티스트 리스트
KPOP_ARTISTS = [
    "BTS", "BLACKPINK", "NewJeans", "IVE", "LE SSERAFIM",
    "Stray Kids", "SEVENTEEN", "EXO", "NCT", "TWICE",
    "aespa", "ZEROBASEONE", "IU", "Taeyeon", "Jisoo",
    "Jungkook", "V", "BIBI", "Zico"
]

# Streamlit Secrets로부터 인증정보 불러오기
client_id = st.secrets["SPOTIFY_CLIENT_ID"]
client_secret = st.secrets["SPOTIFY_CLIENT_SECRET"]

# Spotify 토큰 발급
def get_token(client_id, client_secret):
    auth_str = f"{client_id}:{client_secret}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    res = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    return res.json().get("access_token")

# 국가별 인기 트랙 가져오기 (예: 한국, 미국 등)
def get_top_tracks(token, market="KR"):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://api.spotify.com/v1/browse/new-releases?country={market}&limit=20"
    res = requests.get(url, headers=headers)
    albums = res.json().get("albums", {}).get("items", [])

    tracks = []
    for idx, album in enumerate(albums, start=1):
        name = album["name"]
        artist = ", ".join([a["name"] for a in album["artists"]])
        tracks.append((idx, name, artist))

    df = pd.DataFrame(tracks, columns=["순위", "곡명", "아티스트"])
    return df

# 앱 시작
st.title("🇰🇷 Spotify 인기 앨범 (국가별 - 실시간)")
country = st.selectbox("국가 선택", ["KR", "US", "JP", "GB", "GLOBAL"])
filter_kpop = st.checkbox("K-POP 아티스트만 보기", value=True)

try:
    token = get_token(client_id, client_secret)
    df = get_top_tracks(token, market=country)

    if filter_kpop:
        df = df[df["아티스트"].str.contains("|".join(KPOP_ARTISTS), case=False, na=False)]

    st.write(f"총 {len(df)}곡 표시됨")
    st.dataframe(df)

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")