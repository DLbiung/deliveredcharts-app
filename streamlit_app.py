import streamlit as st
import requests
import pandas as pd

# Spotify API 인증 정보
client_id = "b5017884c27e436b91ac4f802bd38407"
client_secret = "23680682ffb849bdb4f49eb0eb49e46b"

# Access Token 요청 함수
@st.cache_data(ttl=3000)
def get_access_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data, auth=(client_id, client_secret))
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        st.error("Spotify 인증 토큰을 가져오는 데 실패했습니다.")
        return None

# 새 앨범 목록 가져오기
def fetch_spotify_new_releases():
    token = get_access_token()
    if not token:
        return pd.DataFrame()

    url = "https://api.spotify.com/v1/browse/new-releases?limit=20"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        st.error("Spotify API 요청 실패")
        return pd.DataFrame()

    items = response.json()["albums"]["items"]
    data = []
    for item in items:
        title = item["name"]
        artists = ", ".join([artist["name"] for artist in item["artists"]])
        url = item["external_urls"]["spotify"]
        image = item["images"][0]["url"] if item["images"] else ""
        release_date = item["release_date"]
        data.append({
            "앨범": title,
            "아티스트": artists,
            "발매일": release_date,
            "링크": url,
            "이미지": image
        })
    return pd.DataFrame(data)

st.title("🎵 Spotify 신보 차트 (New Releases)")

df = fetch_spotify_new_releases()
if not df.empty:
    st.dataframe(df[["앨범", "아티스트", "발매일", "링크"]])
else:
    st.warning("차트를 불러올 수 없습니다.")
