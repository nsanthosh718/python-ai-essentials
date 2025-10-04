"""
Specialized Agents for Content Analysis Project
"""

import sys
import os
sys.path.append('../agentic-ai')

from agent import Agent, Task
import json
import re
import random
from datetime import datetime
from typing import Dict, List, Any

class ContentCollectorAgent(Agent):
    def __init__(self):
        super().__init__("ContentCollector", ["collect", "fetch", "scrape", "gather"])
        self.sources = ["twitter", "reddit", "news", "reviews"]
    
    def execute_task(self, task: Task) -> Any:
        self.add_memory(f"Collecting content: {task.description}")
        
        # Simulate content collection from different sources
        if "twitter" in task.description.lower():
            return self._collect_twitter_data()
        elif "news" in task.description.lower():
            return self._collect_news_data()
        elif "reviews" in task.description.lower():
            return self._collect_review_data()
        else:
            return self._collect_mixed_content()
    
    def _collect_twitter_data(self):
        # Simulated Twitter data
        tweets = [
            {"text": "Just tried the new AI assistant - absolutely amazing! #AI #tech", "user": "techfan123", "likes": 45},
            {"text": "This AI tool is confusing and hard to use. Not impressed.", "user": "skeptic_user", "likes": 12},
            {"text": "The future of AI is here! Incredible capabilities.", "user": "futurist", "likes": 78},
            {"text": "AI is overhyped. Still prefer human interaction.", "user": "traditional", "likes": 23}
        ]
        return {"source": "twitter", "content": tweets, "count": len(tweets)}
    
    def _collect_news_data(self):
        # Simulated news articles
        articles = [
            {"title": "AI Revolution: New Breakthrough in Natural Language Processing", "summary": "Researchers achieve 95% accuracy in language understanding", "source": "TechNews"},
            {"title": "Concerns Grow Over AI Job Displacement", "summary": "Study shows 30% of jobs at risk from automation", "source": "BusinessDaily"},
            {"title": "AI Helps Doctors Diagnose Diseases Faster", "summary": "Medical AI reduces diagnosis time by 60%", "source": "HealthTech"}
        ]
        return {"source": "news", "content": articles, "count": len(articles)}
    
    def _collect_review_data(self):
        # Simulated product reviews
        reviews = [
            {"text": "Great product! Easy to use and very helpful.", "rating": 5, "product": "AI Assistant"},
            {"text": "Good but could be better. Sometimes gives wrong answers.", "rating": 3, "product": "AI Assistant"},
            {"text": "Excellent! Saves me hours of work every day.", "rating": 5, "product": "AI Assistant"},
            {"text": "Not worth the money. Too many bugs.", "rating": 2, "product": "AI Assistant"}
        ]
        return {"source": "reviews", "content": reviews, "count": len(reviews)}
    
    def _collect_mixed_content(self):
        return {
            "source": "mixed",
            "content": {
                "tweets": self._collect_twitter_data()["content"][:2],
                "articles": self._collect_news_data()["content"][:1],
                "reviews": self._collect_review_data()["content"][:2]
            },
            "count": 5
        }

class SentimentAnalysisAgent(Agent):
    def __init__(self):
        super().__init__("SentimentAnalyzer", ["sentiment", "emotion", "mood", "feeling"])
    
    def execute_task(self, task: Task) -> Any:
        self.add_memory(f"Analyzing sentiment: {task.description}")
        
        # Extract content from task or use sample data
        content = getattr(task, 'content_data', None)
        if not content:
            content = self._get_sample_content()
        
        # Debug: ensure we have content
        if not content or 'content' not in content:
            content = self._get_sample_content()
        
        return self._analyze_sentiment_batch(content)
    
    def _analyze_sentiment_batch(self, content_data):
        results = []
        
        if isinstance(content_data, dict) and "content" in content_data:
            items = content_data["content"]
            if isinstance(items, dict):  # Mixed content
                for source, source_items in items.items():
                    for item in source_items:
                        sentiment = self._analyze_single_item(item)
                        results.append({**sentiment, "source": source, "item": item})
            elif isinstance(items, list):  # Single source
                for item in items:
                    sentiment = self._analyze_single_item(item)
                    results.append({**sentiment, "source": content_data.get("source", "unknown"), "item": item})
        
        # Calculate overall statistics
        sentiments = [r["sentiment"] for r in results]
        sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
        for s in sentiments:
            sentiment_counts[s] += 1
        
        return {
            "individual_results": results,
            "summary": sentiment_counts,
            "total_analyzed": len(results),
            "overall_sentiment": max(sentiment_counts, key=sentiment_counts.get)
        }
    
    def _analyze_single_item(self, item):
        # Extract text from different item types
        text = ""
        if isinstance(item, dict):
            text = item.get("text", item.get("title", item.get("summary", "")))
        else:
            text = str(item)
        
        # Simple sentiment analysis
        positive_words = ["amazing", "great", "excellent", "good", "helpful", "incredible", "love", "fantastic"]
        negative_words = ["bad", "terrible", "awful", "confusing", "wrong", "bugs", "disappointed", "hate"]
        
        text_lower = text.lower()
        pos_score = sum(1 for word in positive_words if word in text_lower)
        neg_score = sum(1 for word in negative_words if word in text_lower)
        
        if pos_score > neg_score:
            sentiment = "positive"
            confidence = min(0.9, 0.6 + (pos_score - neg_score) * 0.1)
        elif neg_score > pos_score:
            sentiment = "negative"
            confidence = min(0.9, 0.6 + (neg_score - pos_score) * 0.1)
        else:
            sentiment = "neutral"
            confidence = 0.5
        
        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "text_preview": text[:100] + "..." if len(text) > 100 else text
        }
    
    def _get_sample_content(self):
        return {
            "source": "sample",
            "content": [
                {"text": "This product is absolutely amazing! I love it."},
                {"text": "Not impressed. Too many issues and bugs."},
                {"text": "It's okay, nothing special but works fine."}
            ]
        }

class TrendAnalysisAgent(Agent):
    def __init__(self):
        super().__init__("TrendAnalyzer", ["trend", "pattern", "analysis", "insights"])
    
    def execute_task(self, task: Task) -> Any:
        self.add_memory(f"Analyzing trends: {task.description}")
        
        # Get sentiment data from previous analysis
        sentiment_data = getattr(task, 'sentiment_data', None)
        if not sentiment_data:
            sentiment_data = self._get_sample_sentiment_data()
        
        return self._analyze_trends(sentiment_data)
    
    def _analyze_trends(self, sentiment_data):
        if not sentiment_data or "individual_results" not in sentiment_data:
            return {"error": "No sentiment data available for trend analysis"}
        
        results = sentiment_data["individual_results"]
        
        # Analyze trends by source
        source_trends = {}
        for result in results:
            source = result.get("source", "unknown")
            if source not in source_trends:
                source_trends[source] = {"positive": 0, "negative": 0, "neutral": 0, "total": 0}
            
            source_trends[source][result["sentiment"]] += 1
            source_trends[source]["total"] += 1
        
        # Calculate percentages
        for source, counts in source_trends.items():
            total = counts["total"]
            if total > 0:
                counts["positive_pct"] = round(counts["positive"] / total * 100, 1)
                counts["negative_pct"] = round(counts["negative"] / total * 100, 1)
                counts["neutral_pct"] = round(counts["neutral"] / total * 100, 1)
        
        # Identify key insights
        insights = []
        for source, data in source_trends.items():
            if data["positive_pct"] > 60:
                insights.append(f"{source.title()} shows strong positive sentiment ({data['positive_pct']}%)")
            elif data["negative_pct"] > 40:
                insights.append(f"{source.title()} has concerning negative sentiment ({data['negative_pct']}%)")
        
        return {
            "source_breakdown": source_trends,
            "key_insights": insights,
            "recommendation": self._generate_recommendation(source_trends),
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def _generate_recommendation(self, source_trends):
        total_positive = sum(data["positive"] for data in source_trends.values())
        total_negative = sum(data["negative"] for data in source_trends.values())
        total_items = sum(data["total"] for data in source_trends.values())
        
        if total_items == 0:
            return "No data available for recommendations"
        
        positive_pct = total_positive / total_items * 100
        
        if positive_pct > 70:
            return "Overall sentiment is very positive. Continue current strategy."
        elif positive_pct > 50:
            return "Sentiment is generally positive but monitor negative feedback areas."
        else:
            return "Negative sentiment detected. Immediate action needed to address concerns."
    
    def _get_sample_sentiment_data(self):
        return {
            "individual_results": [
                {"sentiment": "positive", "confidence": 0.8, "source": "twitter"},
                {"sentiment": "negative", "confidence": 0.7, "source": "reviews"},
                {"sentiment": "positive", "confidence": 0.9, "source": "news"}
            ],
            "summary": {"positive": 2, "negative": 1, "neutral": 0}
        }

class ReportGeneratorAgent(Agent):
    def __init__(self):
        super().__init__("ReportGenerator", ["report", "summary", "document", "generate"])
    
    def execute_task(self, task: Task) -> Any:
        self.add_memory(f"Generating report: {task.description}")
        
        # Collect all analysis data
        content_data = getattr(task, 'content_data', {})
        sentiment_data = getattr(task, 'sentiment_data', {})
        trend_data = getattr(task, 'trend_data', {})
        
        return self._generate_comprehensive_report(content_data, sentiment_data, trend_data)
    
    def _generate_comprehensive_report(self, content_data, sentiment_data, trend_data):
        report = {
            "title": "Smart Content Analysis Report",
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "executive_summary": self._create_executive_summary(sentiment_data, trend_data),
            "data_overview": self._create_data_overview(content_data),
            "sentiment_analysis": self._format_sentiment_results(sentiment_data),
            "trend_analysis": self._format_trend_results(trend_data),
            "recommendations": self._create_recommendations(trend_data)
        }
        
        return report
    
    def _create_executive_summary(self, sentiment_data, trend_data):
        if not sentiment_data or not trend_data:
            return "Analysis completed with limited data availability."
        
        total_analyzed = sentiment_data.get("total_analyzed", 0)
        overall_sentiment = sentiment_data.get("overall_sentiment", "unknown")
        key_insights = trend_data.get("key_insights", [])
        
        summary = f"Analyzed {total_analyzed} content items. "
        summary += f"Overall sentiment: {overall_sentiment}. "
        
        if key_insights:
            summary += f"Key finding: {key_insights[0]}"
        
        return summary
    
    def _create_data_overview(self, content_data):
        if not content_data:
            return "No content data available"
        
        return {
            "source": content_data.get("source", "unknown"),
            "items_collected": content_data.get("count", 0),
            "collection_successful": True
        }
    
    def _format_sentiment_results(self, sentiment_data):
        if not sentiment_data:
            return "No sentiment analysis performed"
        
        return {
            "summary": sentiment_data.get("summary", {}),
            "total_analyzed": sentiment_data.get("total_analyzed", 0),
            "overall_sentiment": sentiment_data.get("overall_sentiment", "unknown")
        }
    
    def _format_trend_results(self, trend_data):
        if not trend_data:
            return "No trend analysis performed"
        
        return {
            "insights": trend_data.get("key_insights", []),
            "recommendation": trend_data.get("recommendation", "No recommendation available")
        }
    
    def _create_recommendations(self, trend_data):
        if not trend_data:
            return ["Collect more data for comprehensive analysis"]
        
        recommendations = [trend_data.get("recommendation", "No specific recommendation")]
        
        # Add general recommendations
        recommendations.extend([
            "Monitor sentiment trends regularly",
            "Address negative feedback promptly",
            "Leverage positive sentiment in marketing"
        ])
        
        return recommendations