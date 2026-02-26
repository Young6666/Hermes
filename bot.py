import os
import requests
import feedparser
import google.generativeai as genai
from datetime import datetime, timedelta, timezone
from dateutil import parser

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# Architecture, Hardware, Performance, AI 분야 집중 키워드
KEYWORDS = [
    # 1. Computer Architecture & Hardware
    "architecture", "microarchitecture", "isa", "risc-v", "arm", "x86",
    "processor", "cpu", "gpu", "tpu", "npu", "fpga", "asic",
    "memory", "dram", "hbm", "cxl", "pim", "processing-in-memory",
    "cache", "interconnect", "chiplet", "wafer", "semiconductor",
    
    # 2. Systems for AI (AI Infra & Optimization)
    "llm inference", "model serving", "training system", "distributed learning",
    "cuda", "rocm", "kernel optimization", "quantization", "model compression",
    "ai accelerator", "machine learning system", "mlsys", "hpc",
    
    # 3. Performance & Optimization
    "performance", "latency", "throughput", "bandwidth", "bottleneck",
    "optimization", "profiling", "parallelism", "concurrency",
    "compiler", "llvm", "simd", "vectorization"
]

RSS_SOURCES = [
    {"name": "GeekNews", "url": "https://news.hada.io/rss"},
    {"name": "Phoronix", "url": "https://www.phoronix.com/rss.php"},
]

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-3-flash')

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
        prompt = f"""
        당신은 Computer Architecture, Hardware, AI System 분야의 전문 연구원입니다.
        아래 뉴스 내용을 동료 대학원생에게 브리핑하기 위해, 
        '시스템 및 하드웨어 관점'에서 성능 영향, 아키텍처 변화, 기술적 특징 위주로 **3줄 이내로 한글 요약**해주세요.

        제목: {title}
        내용: {content}
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini 호출 오류: {e}")
        return "요약 실패 (원문 확인 요망)"

def fetch_and_process_news():
    time_window = datetime.now(timezone.utc) - timedelta(hours=8)
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