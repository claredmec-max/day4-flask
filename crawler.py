import sys

import requests
from bs4 import BeautifulSoup, FeatureNotFound

RSS_URL = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"


def _clean_text(value: str) -> str:
    return " ".join(value.split()) if value else ""


def _safe_console_text(value: str) -> str:
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    return value.encode(encoding, errors="replace").decode(encoding, errors="replace")


def fetch_news(limit: int = 10):
    response = requests.get(RSS_URL, timeout=(3.05, 10))
    response.raise_for_status()

    try:
        soup = BeautifulSoup(response.content, "xml")
    except FeatureNotFound:
        soup = BeautifulSoup(response.content, "html.parser")

    items = []
    for item in soup.find_all("item")[:limit]:
        title = _clean_text(item.title.get_text()) if item.title else "(제목 없음)"
        if item.description:
            summary_soup = BeautifulSoup(item.description.get_text(), "html.parser")
            summary = _clean_text(summary_soup.get_text(" ", strip=True))
        else:
            summary = ""
        link = _clean_text(item.link.get_text()) if item.link else ""
        pub_date = _clean_text(item.pubDate.get_text()) if item.pubDate else ""

        items.append(
            {
                "title": title,
                "summary": summary,
                "link": link,
                "pub_date": pub_date,
            }
        )

    return items


def print_news(news_items):
    print("=" * 90)
    print(f"Google News 한국어 RSS 상위 {len(news_items)}건")
    print("=" * 90)

    for idx, news in enumerate(news_items, start=1):
        print(f"\n[{idx}] {_safe_console_text(news['title'])}")
        print(f"요약      : {_safe_console_text(news['summary'])}")
        print(f"링크      : {_safe_console_text(news['link'])}")
        print(f"발행시간  : {_safe_console_text(news['pub_date'])}")
        print("-" * 90)


def main():
    try:
        news_items = fetch_news(limit=10)
        print_news(news_items)
    except requests.RequestException as e:
        print(f"RSS 요청 중 오류가 발생했습니다: {e}")


if __name__ == "__main__":
    main()
