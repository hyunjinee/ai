import feedparser
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
from urllib.parse import quote
from typing import TypedDict, List, Dict, Annotated
from operator import add

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

from langgraph.graph import StateGraph, START, END

finbert_model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")
finbert_tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")

labels = ['Positive', 'Negative', 'Neutral']

# LangGraph State 정의
class NewsAnalysisState(TypedDict):
    queries: List[str]
    num_articles_per_query: int
    articles: Annotated[List[Dict], add]  # 리스트를 누적하기 위해 add 연산자 사용
    current_query_index: int
    sentiment_summary: Dict[str, int]
    analysis_complete: bool

def fetch_news(query, num_articles=10):
    rss_url = f"https://news.google.com/rss/search?q={quote(query)}"
    feed = feedparser.parse(rss_url)
    news_items = feed.entries[:num_articles]

    articles = []
    for item in news_items:
        title = item.title
        link = item.link
        published = item.published
        content = fetch_article_content(link)
        
        articles.append({
            "title": title,
            "link": link,
            "published": published,
            "content": content
        })

    return articles

def fetch_article_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        paragraphs = soup.find_all('p')
        content = ' '.join([p.get_text() for p in paragraphs])
        return content.strip()
    except requests.RequestException:
        return "Content not retrieved."

def analyze_sentiment(text):

    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    polarity = scores['compound']

    # analysis = TextBlob(text)
    # polarity = analysis.sentiment.polarity

    if polarity > 0.05:
        sentiment = 'Positive'
    elif polarity < -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    return polarity, sentiment

# def analyze_sentiment(text):
#     if not text.strip():
#         return 0.0, 'Neutral'

#     inputs = finbert_tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
#     with torch.no_grad():
#         outputs = finbert_model(**inputs)

#     logits = outputs.logits
#     probabilities = torch.softmax(logits, dim=1).numpy()[0]
#     max_index = np.argmax(probabilities)
#     sentiment = labels[max_index]
#     confidence = probabilities[max_index]

#     return confidence, sentiment


def summarize_sentiments(articles):
    summary = {
        "Positive": 0,
        "Negative": 0,
        "Neutral": 0
    }

    for article in articles:
        # print("-"*25)
        # print(f"\n--- Analyzing Article: {article['title']} ---")
        # print(f"Published: {article['published']}")
        # print(article['content'])
        _, sentiment = analyze_sentiment(article['title']) # + " " + article['content'])
        summary[sentiment] += 1

    total = len(articles)
    print("\n--- Market Sentiment Summary ---")
    print(f"Total articles analyzed: {total}")
    for sentiment, count in summary.items():
        percent = (count / total) * 100
        print(f"{sentiment}: {count} ({percent:.2f}%)")

# LangGraph 노드 함수들
def fetch_news_node(state: NewsAnalysisState) -> NewsAnalysisState:
    """현재 쿼리로 뉴스 기사를 가져오는 노드"""
    current_index = state.get("current_query_index", 0)
    queries = state["queries"]
    
    if current_index >= len(queries):
        return {"analysis_complete": True}
    
    query = queries[current_index]
    num_articles = state["num_articles_per_query"]
    
    print(f"\n[노드 1: 뉴스 가져오기] '{query}' 쿼리로 기사를 가져오는 중...")
    
    rss_url = f"https://news.google.com/rss/search?q={quote(query)}"
    feed = feedparser.parse(rss_url)
    news_items = feed.entries[:num_articles]

    articles = []
    for item in news_items:
        title = item.title
        link = item.link
        published = item.published
        content = fetch_article_content(link)
        
        articles.append({
            "title": title,
            "link": link,
            "published": published,
            "content": content
        })
    
    print(f"  ✓ {len(articles)}개의 기사를 가져왔습니다.")
    
    return {
        "articles": articles,
        "current_query_index": current_index + 1,
    }

def analyze_sentiments_node(state: NewsAnalysisState) -> NewsAnalysisState:
    """모든 기사의 감정을 분석하는 노드"""
    articles = state.get("articles", [])
    
    print(f"\n[노드 2: 감정 분석] {len(articles)}개의 기사를 분석하는 중...")
    
    for idx, article in enumerate(articles, 1):
        polarity, sentiment = analyze_sentiment(article['title'])
        article['polarity'] = polarity
        article['sentiment'] = sentiment
        
        if idx % 10 == 0:
            print(f"  진행: {idx}/{len(articles)} 기사 분석 완료")
    
    print(f"  ✓ 모든 기사 분석 완료")
    
    return {"articles": articles}

def summarize_results_node(state: NewsAnalysisState) -> NewsAnalysisState:
    """감정 분석 결과를 요약하는 노드"""
    articles = state.get("articles", [])
    
    print(f"\n[노드 3: 결과 요약] 분석 결과를 요약하는 중...")
    
    summary = {
        "Positive": 0,
        "Negative": 0,
        "Neutral": 0
    }

    for article in articles:
        sentiment = article.get('sentiment', 'Neutral')
        summary[sentiment] += 1

    total = len(articles)
    print("\n" + "="*50)
    print("시장 감정 분석 요약")
    print("="*50)
    print(f"총 분석 기사 수: {total}")
    print("-"*50)
    for sentiment, count in summary.items():
        percent = (count / total) * 100 if total > 0 else 0
        bar = "█" * int(percent / 2)
        print(f"{sentiment:>8}: {count:3d} ({percent:5.2f}%) {bar}")
    print("="*50)
    
    return {
        "sentiment_summary": summary,
        "analysis_complete": True
    }

def should_continue(state: NewsAnalysisState) -> str:
    """다음 쿼리를 처리할지, 감정 분석으로 넘어갈지 결정하는 조건부 엣지"""
    current_index = state.get("current_query_index", 0)
    queries = state["queries"]
    
    if current_index < len(queries):
        return "fetch_more"
    else:
        return "analyze"

def create_workflow() -> StateGraph:
    """LangGraph 워크플로우를 생성합니다"""
    
    # StateGraph 생성
    workflow = StateGraph(NewsAnalysisState)
    
    # 노드 추가
    workflow.add_node("fetch_news", fetch_news_node)
    workflow.add_node("analyze_sentiments", analyze_sentiments_node)
    workflow.add_node("summarize_results", summarize_results_node)
    
    # 엣지 추가
    workflow.add_edge(START, "fetch_news")
    
    # 조건부 엣지: 뉴스를 더 가져올지, 아니면 분석으로 넘어갈지 결정
    workflow.add_conditional_edges(
        "fetch_news",
        should_continue,
        {
            "fetch_more": "fetch_news",  # 다시 fetch_news로 돌아가서 다음 쿼리 처리
            "analyze": "analyze_sentiments"  # 모든 쿼리를 처리했으면 감정 분석으로
        }
    )
    
    # 감정 분석 후 요약으로
    workflow.add_edge("analyze_sentiments", "summarize_results")
    
    # 요약 후 종료
    workflow.add_edge("summarize_results", END)
    
    return workflow.compile()

def main():
    """LangGraph를 사용한 뉴스 감정 분석 메인 함수"""
    
    print("\n" + "="*70)
    print("LangGraph 기반 뉴스 감정 분석 워크플로우")
    print("="*70)
    
    # 초기 상태 설정
    initial_state: NewsAnalysisState = {
        "queries": [
            "gold market",
            "gold price",
            "gold news",
            "gold trends",
            "gold analysis",
            "gold forecast",
            "gold investment"
        ],
        "num_articles_per_query": 10,
        "articles": [],
        "current_query_index": 0,
        "sentiment_summary": {},
        "analysis_complete": False
    }
    
    # 워크플로우 생성
    app = create_workflow()
    
    # 워크플로우 실행
    print("\n워크플로우를 시작합니다...\n")
    final_state = app.invoke(initial_state)
    
    # 최종 결과 출력
    print("\n" + "="*70)
    print("워크플로우 완료!")
    print("="*70)
    print(f"\n총 수집된 기사: {len(final_state['articles'])}개")
    print(f"처리된 쿼리: {final_state['current_query_index']}/{len(final_state['queries'])}")
    
    # 상세 기사 정보 출력 (선택사항)
    if input("\n상세 기사 정보를 보시겠습니까? (y/n): ").lower() == 'y':
        print("\n" + "="*70)
        print("기사 상세 정보")
        print("="*70)
        for idx, article in enumerate(final_state['articles'], 1):
            print(f"\n[기사 {idx}]")
            print(f"제목: {article['title']}")
            print(f"링크: {article['link']}")
            print(f"발행: {article['published']}")
            print(f"감정: {article.get('sentiment', 'N/A')} (극성: {article.get('polarity', 0):.2f})")

if __name__ == "__main__":
    main()