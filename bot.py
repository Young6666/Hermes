import os
import requests
import feedparser
import google.generativeai as genai
from datetime import datetime, timedelta, timezone
from dateutil import parser

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

from config import KEYWORDS, RSS_SOURCES, GEMINI_MODEL, GEMINI_PROMPT_TEMPLATE

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)

def send_slack_message(text):
    if not SLACK_WEBHOOK_URL:
        print("Slack Webhook URL이 없습니다.")
        return
    payload = {"text": text}
    try:
        requests.post(SLACK_WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"Slack 전송 실패: {e}")

def summarize_with_gemini(title, content):
    if not GOOGLE_API_KEY:
        return "API 키가 없어 요약할 수 없습니다."
    
    try:
        prompt = GEMINI_PROMPT_TEMPLATE.format(title=title, content=content)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini 호출 오류: {e}")
        return "요약 실패 (원문 확인 요망)"

def fetch_and_process_news():
    time_window = datetime.now(timezone.utc) - timedelta(hours=25)
    print(f"[{datetime.now()}] 뉴스 수집 시작 (기준: {time_window} 이후)")

    count = 0
    for source in RSS_SOURCES:
        print(f"Checking {source['name']}...")
        try:
            feed = feedparser.parse(source["url"])
            
            for entry in feed.entries[:10]: 
                try:
                    published_time = parser.parse(entry.published)
                    if published_time.tzinfo is None:
                        published_time = published_time.replace(tzinfo=timezone.utc)
                except:
                    continue 

                if published_time < time_window:
                    continue

                full_text = (entry.title + " " + entry.get('summary', '')).lower()
                if any(k in full_text for k in KEYWORDS):
                    print(f" -> [Hit] {entry.title}")
                    
                    summary = summarize_with_gemini(entry.title, entry.get('summary', ''))
                    
                    message = (
                        f"📢 *[{source['name']}] Tech Update*\n"
                        f"👉 <{entry.link}|*{entry.title}*>\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                        f"{summary}\n"
                    )
                    send_slack_message(message)
                    count += 1
                    if (count >= 3):
                        return
                    
        except Exception as e:
            print(f"{source['name']} 처리 중 오류 발생: {e}")

if __name__ == "__main__":
    fetch_and_process_news()