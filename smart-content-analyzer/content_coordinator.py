"""
Smart Content Analysis Coordinator
Orchestrates the complete content analysis pipeline
"""

import sys
import os
sys.path.append('../agentic-ai')

from coordinator import AgentCoordinator
from agent import Task
from content_agents import ContentCollectorAgent, SentimentAnalysisAgent, TrendAnalysisAgent, ReportGeneratorAgent
import json
import time

class ContentAnalysisCoordinator(AgentCoordinator):
    def __init__(self):
        super().__init__()
        # Replace default agents with specialized content analysis agents
        self.agents = [
            ContentCollectorAgent(),
            SentimentAnalysisAgent(),
            TrendAnalysisAgent(),
            ReportGeneratorAgent()
        ]
        self.analysis_results = {}
    
    def run_complete_analysis(self, content_source="mixed"):
        """Run the complete content analysis pipeline"""
        print(f"🚀 Starting Smart Content Analysis for: {content_source}")
        
        # Step 1: Content Collection
        print("\n📊 Step 1: Collecting Content...")
        collection_task = Task(
            id="collect_content",
            description=f"Collect content from {content_source} sources",
            priority=3
        )
        self.task_queue.append(collection_task)
        collection_result = self.execute_next_task()
        
        if collection_result["status"] != "success":
            return {"error": "Content collection failed", "details": collection_result}
        
        content_data = collection_result["result"]
        self.analysis_results["content"] = content_data
        print(f"✅ Collected {content_data.get('count', 0)} items from {content_data.get('source', 'unknown')}")
        
        # Step 2: Sentiment Analysis
        print("\n💭 Step 2: Analyzing Sentiment...")
        sentiment_task = Task(
            id="analyze_sentiment",
            description="Analyze sentiment of collected content",
            priority=2
        )
        sentiment_task.content_data = content_data
        self.task_queue.append(sentiment_task)
        sentiment_result = self.execute_next_task()
        
        if sentiment_result["status"] != "success":
            return {"error": "Sentiment analysis failed", "details": sentiment_result}
        
        sentiment_data = sentiment_result["result"]
        self.analysis_results["sentiment"] = sentiment_data
        print(f"✅ Analyzed {sentiment_data.get('total_analyzed', 0)} items")
        print(f"   Overall sentiment: {sentiment_data.get('overall_sentiment', 'unknown')}")
        
        # Step 3: Trend Analysis
        print("\n📈 Step 3: Analyzing Trends...")
        trend_task = Task(
            id="analyze_trends",
            description="Identify trends and patterns in sentiment data",
            priority=2
        )
        trend_task.sentiment_data = sentiment_data
        self.task_queue.append(trend_task)
        trend_result = self.execute_next_task()
        
        if trend_result["status"] != "success":
            return {"error": "Trend analysis failed", "details": trend_result}
        
        trend_data = trend_result["result"]
        self.analysis_results["trends"] = trend_data
        print(f"✅ Identified {len(trend_data.get('key_insights', []))} key insights")
        
        # Step 4: Report Generation
        print("\n📋 Step 4: Generating Report...")
        report_task = Task(
            id="generate_report",
            description="Generate comprehensive analysis report",
            priority=1
        )
        report_task.content_data = content_data
        report_task.sentiment_data = sentiment_data
        report_task.trend_data = trend_data
        self.task_queue.append(report_task)
        report_result = self.execute_next_task()
        
        if report_result["status"] != "success":
            return {"error": "Report generation failed", "details": report_result}
        
        report_data = report_result["result"]
        self.analysis_results["report"] = report_data
        print("✅ Report generated successfully")
        
        return {
            "status": "success",
            "analysis_complete": True,
            "results": self.analysis_results,
            "summary": {
                "content_items": content_data.get("count", 0),
                "sentiment_analyzed": sentiment_data.get("total_analyzed", 0),
                "overall_sentiment": sentiment_data.get("overall_sentiment", "unknown"),
                "key_insights": len(trend_data.get("key_insights", [])),
                "report_generated": True
            }
        }
    
    def analyze_custom_content(self, content_text, source="custom"):
        """Analyze custom text content"""
        print(f"🔍 Analyzing custom content...")
        
        # Create custom content data
        custom_content = {
            "source": source,
            "content": [{"text": content_text}],
            "count": 1
        }
        
        # Run sentiment analysis
        sentiment_task = Task(
            id="analyze_custom_sentiment",
            description="Analyze sentiment of custom content",
            priority=2
        )
        sentiment_task.content_data = custom_content
        self.task_queue.append(sentiment_task)
        sentiment_result = self.execute_next_task()
        
        if sentiment_result["status"] == "success":
            sentiment_data = sentiment_result["result"]
            result = sentiment_data["individual_results"][0] if sentiment_data["individual_results"] else {}
            
            return {
                "text": content_text,
                "sentiment": result.get("sentiment", "unknown"),
                "confidence": result.get("confidence", 0),
                "analysis_successful": True
            }
        else:
            return {
                "text": content_text,
                "error": "Analysis failed",
                "analysis_successful": False
            }
    
    def get_analysis_summary(self):
        """Get a quick summary of the last analysis"""
        if not self.analysis_results:
            return "No analysis has been performed yet"
        
        summary = []
        
        if "content" in self.analysis_results:
            content = self.analysis_results["content"]
            summary.append(f"📊 Collected {content.get('count', 0)} items from {content.get('source', 'unknown')}")
        
        if "sentiment" in self.analysis_results:
            sentiment = self.analysis_results["sentiment"]
            summary.append(f"💭 Overall sentiment: {sentiment.get('overall_sentiment', 'unknown')}")
            summary.append(f"   Analyzed {sentiment.get('total_analyzed', 0)} items")
        
        if "trends" in self.analysis_results:
            trends = self.analysis_results["trends"]
            insights = trends.get("key_insights", [])
            if insights:
                summary.append(f"📈 Key insight: {insights[0]}")
        
        return "\n".join(summary)
    
    def save_results(self, filename="analysis_results.json"):
        """Save analysis results to file"""
        if not self.analysis_results:
            return {"error": "No results to save"}
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.analysis_results, f, indent=2, default=str)
            return {"success": True, "filename": filename}
        except Exception as e:
            return {"error": f"Failed to save results: {str(e)}"}

def run_demo_analysis():
    """Run a demonstration of the content analysis system"""
    coordinator = ContentAnalysisCoordinator()
    
    print("🎯 Smart Content Analysis System Demo")
    print("=" * 50)
    
    # Run complete analysis
    result = coordinator.run_complete_analysis("mixed")
    
    if result.get("status") == "success":
        print(f"\n🎉 Analysis Complete!")
        print(f"📊 Summary: {result['summary']}")
        
        # Show key insights
        if "trends" in coordinator.analysis_results:
            insights = coordinator.analysis_results["trends"].get("key_insights", [])
            if insights:
                print(f"\n💡 Key Insights:")
                for insight in insights:
                    print(f"   • {insight}")
        
        # Show recommendations
        if "report" in coordinator.analysis_results:
            recommendations = coordinator.analysis_results["report"].get("recommendations", [])
            if recommendations:
                print(f"\n📋 Recommendations:")
                for rec in recommendations[:3]:  # Show top 3
                    print(f"   • {rec}")
        
        # Save results
        save_result = coordinator.save_results()
        if save_result.get("success"):
            print(f"\n💾 Results saved to: {save_result['filename']}")
    
    else:
        print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
    
    return coordinator

if __name__ == "__main__":
    run_demo_analysis()