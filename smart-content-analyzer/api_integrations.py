"""
Real API Integrations for Content Collection
"""

import requests
import json
import os
from datetime import datetime
import time

class NewsAPIClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2"
    
    def get_headlines(self, query="AI", language="en", page_size=10):
        """Get news headlines from NewsAPI"""
        if not self.api_key:
            return self._mock_news_response(query)
        
        try:
            url = f"{self.base_url}/everything"
            params = {
                "q": query,
                "language": language,
                "pageSize": page_size,
                "sortBy": "publishedAt",
                "apiKey": self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self._format_news_response(data)
            
        except Exception as e:
            print(f"NewsAPI error: {e}")
            return self._mock_news_response(query)
    
    def _mock_news_response(self, query):
        """Mock news response when API key is not available"""
        mock_articles = [
            {
                "title": f"Latest developments in {query} technology",
                "description": f"New breakthrough in {query} research shows promising results",
                "content": f"Researchers have made significant progress in {query} technology, with applications spanning multiple industries.",
                "source": {"name": "TechNews"},
                "publishedAt": datetime.now().isoformat(),
                "url": "https://example.com/news1"
            },
            {
                "title": f"{query} market analysis and future predictions",
                "description": f"Industry experts analyze the current state of {query} market",
                "content": f"The {query} market continues to grow rapidly, with new players entering the space and established companies expanding their offerings.",
                "source": {"name": "MarketWatch"},
                "publishedAt": datetime.now().isoformat(),
                "url": "https://example.com/news2"
            }
        ]
        
        return {
            "status": "ok",
            "totalResults": len(mock_articles),
            "articles": mock_articles,
            "mock_data": True
        }
    
    def _format_news_response(self, data):
        """Format NewsAPI response for our system"""
        if data.get("status") != "ok":
            return {"error": "NewsAPI request failed"}
        
        formatted_articles = []
        for article in data.get("articles", []):
            formatted_articles.append({
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "content": article.get("content", ""),
                "source": article.get("source", {}).get("name", "Unknown"),
                "publishedAt": article.get("publishedAt", ""),
                "url": article.get("url", "")
            })
        
        return {
            "status": "ok",
            "totalResults": data.get("totalResults", 0),
            "articles": formatted_articles,
            "mock_data": False
        }

class RedditAPIClient:
    def __init__(self):
        self.base_url = "https://www.reddit.com"
    
    def get_posts(self, subreddit="artificial", limit=10):
        """Get Reddit posts (using public JSON API)"""
        try:
            url = f"{self.base_url}/r/{subreddit}/hot.json"
            params = {"limit": limit}
            
            headers = {"User-Agent": "ContentAnalyzer/1.0"}
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self._format_reddit_response(data, subreddit)
            
        except Exception as e:
            print(f"Reddit API error: {e}")
            return self._mock_reddit_response(subreddit)
    
    def _mock_reddit_response(self, subreddit):
        """Mock Reddit response"""
        mock_posts = [
            {
                "title": "What's your opinion on the latest AI developments?",
                "text": "I've been following AI research and the recent breakthroughs are incredible. What do you think about the future implications?",
                "subreddit": subreddit,
                "score": 245,
                "num_comments": 67,
                "created_utc": time.time(),
                "author": "ai_enthusiast"
            },
            {
                "title": "AI concerns and ethical considerations",
                "text": "While AI progress is exciting, we need to address the ethical implications and potential risks. What safeguards should be in place?",
                "subreddit": subreddit,
                "score": 189,
                "num_comments": 43,
                "created_utc": time.time(),
                "author": "ethics_researcher"
            }
        ]
        
        return {
            "status": "success",
            "subreddit": subreddit,
            "posts": mock_posts,
            "mock_data": True
        }
    
    def _format_reddit_response(self, data, subreddit):
        """Format Reddit API response"""
        posts = []
        
        for post_data in data.get("data", {}).get("children", []):
            post = post_data.get("data", {})
            
            posts.append({
                "title": post.get("title", ""),
                "text": post.get("selftext", ""),
                "subreddit": subreddit,
                "score": post.get("score", 0),
                "num_comments": post.get("num_comments", 0),
                "created_utc": post.get("created_utc", 0),
                "author": post.get("author", "unknown")
            })
        
        return {
            "status": "success",
            "subreddit": subreddit,
            "posts": posts,
            "mock_data": False
        }

class TwitterAPIClient:
    def __init__(self, bearer_token=None):
        self.bearer_token = bearer_token or os.getenv("TWITTER_BEARER_TOKEN")
        self.base_url = "https://api.twitter.com/2"
    
    def search_tweets(self, query="AI", max_results=10):
        """Search tweets using Twitter API v2"""
        if not self.bearer_token:
            return self._mock_twitter_response(query)
        
        try:
            url = f"{self.base_url}/tweets/search/recent"
            params = {
                "query": query,
                "max_results": max_results,
                "tweet.fields": "created_at,public_metrics,author_id"
            }
            
            headers = {"Authorization": f"Bearer {self.bearer_token}"}
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self._format_twitter_response(data)
            
        except Exception as e:
            print(f"Twitter API error: {e}")
            return self._mock_twitter_response(query)
    
    def _mock_twitter_response(self, query):
        """Mock Twitter response"""
        mock_tweets = [
            {
                "text": f"Just discovered this amazing {query} tool! It's revolutionizing how I work. Highly recommend checking it out! #AI #technology",
                "created_at": datetime.now().isoformat(),
                "public_metrics": {"like_count": 45, "retweet_count": 12, "reply_count": 8},
                "author_id": "user123"
            },
            {
                "text": f"Concerned about the rapid pace of {query} development. We need more discussion about ethics and safety measures.",
                "created_at": datetime.now().isoformat(),
                "public_metrics": {"like_count": 23, "retweet_count": 6, "reply_count": 15},
                "author_id": "user456"
            }
        ]
        
        return {
            "data": mock_tweets,
            "meta": {"result_count": len(mock_tweets)},
            "mock_data": True
        }
    
    def _format_twitter_response(self, data):
        """Format Twitter API response"""
        tweets = []
        
        for tweet in data.get("data", []):
            tweets.append({
                "text": tweet.get("text", ""),
                "created_at": tweet.get("created_at", ""),
                "public_metrics": tweet.get("public_metrics", {}),
                "author_id": tweet.get("author_id", "")
            })
        
        return {
            "data": tweets,
            "meta": data.get("meta", {}),
            "mock_data": False
        }

class APIManager:
    """Centralized API management"""
    
    def __init__(self):
        self.news_client = NewsAPIClient()
        self.reddit_client = RedditAPIClient()
        self.twitter_client = TwitterAPIClient()
    
    def collect_from_all_sources(self, query="AI", limit=5):
        """Collect content from all available sources"""
        results = {}
        
        # Collect news
        print("📰 Collecting news articles...")
        news_data = self.news_client.get_headlines(query, page_size=limit)
        results["news"] = {
            "data": news_data.get("articles", []),
            "count": len(news_data.get("articles", [])),
            "mock": news_data.get("mock_data", False)
        }
        
        # Collect Reddit posts
        print("🔴 Collecting Reddit posts...")
        reddit_data = self.reddit_client.get_posts("artificial", limit=limit)
        results["reddit"] = {
            "data": reddit_data.get("posts", []),
            "count": len(reddit_data.get("posts", [])),
            "mock": reddit_data.get("mock_data", False)
        }
        
        # Collect tweets
        print("🐦 Collecting tweets...")
        twitter_data = self.twitter_client.search_tweets(query, max_results=limit)
        results["twitter"] = {
            "data": twitter_data.get("data", []),
            "count": len(twitter_data.get("data", [])),
            "mock": twitter_data.get("mock_data", False)
        }
        
        total_items = sum(source["count"] for source in results.values())
        
        return {
            "sources": results,
            "total_items": total_items,
            "query": query,
            "collected_at": datetime.now().isoformat()
        }
    
    def get_api_status(self):
        """Check which APIs are available"""
        status = {
            "news_api": bool(self.news_client.api_key),
            "twitter_api": bool(self.twitter_client.bearer_token),
            "reddit_api": True,  # Public API, always available
            "mock_mode": not (self.news_client.api_key and self.twitter_client.bearer_token)
        }
        
        return status