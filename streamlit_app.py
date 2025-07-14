import streamlit as st
import requests
import pandas as pd

# 실시간 Spotify 최신 앨범 데이터 가져오기
def fetch_new_releases(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = "https://api.spotify.com/v1/browse/new-releases?limit=20"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        st.error(f"Spotify API 오류 발생: {response.status_code}")
        return pd.DataFrame()

    data = response.json()
    albums = data.get("albums", {}).get("items", [])

    album_data = []
    for album in albums:
        album_name = album["name"]
        artist_names = ", ".join(artist["name"] for artist in album["artists"])
        release_date = album["release_date"]
        image_url = album["images"][0]["url"] if album["images"] else ""

        album_data.append({
            "앨범": album_name,
            "아티스트": artist_names,
            "발매일": release_date,
            "커버": image_url
        })

    return pd.DataFrame(album_data)

# Streamlit 앱 인터페이스
st.title("Spotify 최신 앨범 차트 (New Releases)")
access_token = st.text_input("Spotify Access Token을 입력하세요", type="password")

if access_token:
    df = fetch_new_releases(access_token)
    if not df.empty:
        for _, row in df.iterrows():
            st.image(row["커버"], width=150)
            st.markdown(f"**{row['앨범']}** by {row['아티스트']} ({row['발매일']})")
            st.markdown("---")
    else:
        st.warning("데이터를 불러오지 못했습니다. Access Token을 확인하세요.")
else:
    st.info("Spotify Access Token을 입력해주세요.")
