import requests
import pandas as pd
from bs4 import BeautifulSoup

def fetch_spotifycharts_chart(country='global'):
    """
    SpotifyCharts.com에서 최신 일간 차트를 크롤링하는 함수.
    :param country: 'global', 'kr', 'us' 등의 국가 코드
    :return: pandas DataFrame
    """
    url = f"https://spotifycharts.com/regional/{country}/daily/latest"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            print(f"요청 실패: 상태 코드 {res.status_code}")
            return None

        soup = BeautifulSoup(res.text, 'html.parser')
        table = soup.find("table", {"class": "chart-table"})
        if table is None:
            print("차트 테이블을 찾을 수 없습니다.")
            return None

        rows = table.select("tbody tr")
        chart_data = []

        for row in rows:
            try:
                rank = int(row.select_one(".chart-table-position").text.strip())
                title = row.select_one(".chart-table-track strong").text.strip()
                artist = row.select_one(".chart-table-track span").text.replace("by ", "").strip()
                streams = row.select_one(".chart-table-streams").text.strip().replace(",", "")
                chart_data.append({
                    "순위": rank,
                    "곡명": title,
                    "아티스트": artist,
                    "스트리밍 수": int(streams)
                })
            except Exception as e:
                print(f"행 처리 오류: {e}")
                continue

        return pd.DataFrame(chart_data)

    except Exception as e:
        print(f"크롤링 오류: {e}")
        return None
