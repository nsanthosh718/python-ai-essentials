"""
LLM-powered Agent for Natural Language Processing
"""

import json
import re
from agent import Agent, Task
from typing import Dict, List, Any, Optional

class LLMAgent(Agent):
    def __init__(self, model_type="local"):
        super().__init__("LLMAgent", ["nlp", "text", "language", "chat", "analyze", "summarize"])
        self.model_type = model_type
        self.conversation_history = []
    
    def execute_task(self, task: Task) -> Any:
        self.add_memory(f"Processing NLP task: {task.description}")
        
        # Route to appropriate NLP function
        if "summarize" in task.description.lower():
            return self._summarize_text(task.description)
        elif "sentiment" in task.description.lower():
            return self._analyze_sentiment(task.description)
        elif "extract" in task.description.lower():
            return self._extract_entities(task.description)
        elif "translate" in task.description.lower():
            return self._translate_text(task.description)
        elif "chat" in task.description.lower() or "respond" in task.description.lower():
            return self._chat_response(task.description)
        else:
            return self._general_nlp_processing(task.description)
    
    def _summarize_text(self, text: str) -> Dict:
        # Simple extractive summarization
        sentences = text.split('.')
        key_sentences = [s.strip() for s in sentences if len(s.strip()) > 20][:3]
        
        return {
            "summary": ". ".join(key_sentences),
            "original_length": len(text),
            "summary_length": len(". ".join(key_sentences)),
            "compression_ratio": round(len(". ".join(key_sentences)) / len(text), 2)
        }
    
    def _analyze_sentiment(self, text: str) -> Dict:
        # Simple rule-based sentiment analysis
        positive_words = ["good", "great", "excellent", "amazing", "wonderful", "fantastic", "love", "like"]
        negative_words = ["bad", "terrible", "awful", "hate", "dislike", "horrible", "worst"]
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            sentiment = "positive"
            confidence = min(0.9, 0.5 + (pos_count - neg_count) * 0.1)
        elif neg_count > pos_count:
            sentiment = "negative"
            confidence = min(0.9, 0.5 + (neg_count - pos_count) * 0.1)
        else:
            sentiment = "neutral"
            confidence = 0.5
        
        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "positive_indicators": pos_count,
            "negative_indicators": neg_count
        }
    
    def _extract_entities(self, text: str) -> Dict:
        # Simple entity extraction using regex
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'\b\d{3}-\d{3}-\d{4}\b|\b\(\d{3}\)\s*\d{3}-\d{4}\b'
        date_pattern = r'\b\d{1,2}/\d{1,2}/\d{4}\b|\b\d{4}-\d{2}-\d{2}\b'
        
        entities = {
            "emails": re.findall(email_pattern, text),
            "phones": re.findall(phone_pattern, text),
            "dates": re.findall(date_pattern, text),
            "numbers": re.findall(r'\b\d+\.?\d*\b', text)
        }
        
        return {
            "entities": entities,
            "entity_count": sum(len(v) for v in entities.values()),
            "text_length": len(text)
        }
    
    def _translate_text(self, text: str) -> Dict:
        # Mock translation (in real implementation, use translation API)
        translations = {
            "hello": "hola",
            "goodbye": "adiós",
            "thank you": "gracias",
            "please": "por favor"
        }
        
        translated = text.lower()
        for eng, spa in translations.items():
            translated = translated.replace(eng, spa)
        
        return {
            "original": text,
            "translated": translated,
            "source_language": "en",
            "target_language": "es",
            "confidence": 0.8
        }
    
    def _chat_response(self, message: str) -> Dict:
        # Simple chatbot responses
        responses = {
            "hello": "Hello! How can I help you today?",
            "how are you": "I'm doing well, thank you for asking!",
            "what can you do": "I can help with text analysis, summarization, sentiment analysis, and more!",
            "goodbye": "Goodbye! Have a great day!",
            "help": "I can assist with various NLP tasks. Just describe what you need!"
        }
        
        message_lower = message.lower()
        response = "I understand you're asking about something. Could you be more specific?"
        
        for key, resp in responses.items():
            if key in message_lower:
                response = resp
                break
        
        self.conversation_history.append({"user": message, "assistant": response})
        
        return {
            "response": response,
            "conversation_turn": len(self.conversation_history),
            "context_maintained": True
        }
    
    def _general_nlp_processing(self, text: str) -> Dict:
        # General text analysis
        words = text.split()
        sentences = text.split('.')
        
        return {
            "word_count": len(words),
            "sentence_count": len([s for s in sentences if s.strip()]),
            "avg_word_length": round(sum(len(word) for word in words) / len(words), 2) if words else 0,
            "readability_score": min(100, max(0, 100 - len(words) * 0.5)),
            "language_detected": "en"
        }

class TaskInterpreter:
    """Interprets natural language task descriptions"""
    
    def __init__(self):
        self.task_patterns = {
            "data": ["analyze data", "process data", "clean data", "load data"],
            "ml": ["train model", "predict", "machine learning", "classification"],
            "nlp": ["summarize", "translate", "sentiment", "text analysis"],
            "plan": ["create plan", "schedule", "organize", "coordinate"]
        }
    
    def interpret_task(self, description: str) -> Dict:
        """Convert natural language to structured task"""
        desc_lower = description.lower()
        
        # Determine task type
        task_type = "general"
        confidence = 0.5
        
        for category, patterns in self.task_patterns.items():
            for pattern in patterns:
                if pattern in desc_lower:
                    task_type = category
                    confidence = 0.9
                    break
            if confidence > 0.8:
                break
        
        # Extract priority indicators
        priority = 1
        if any(word in desc_lower for word in ["urgent", "asap", "critical", "important"]):
            priority = 3
        elif any(word in desc_lower for word in ["soon", "priority", "needed"]):
            priority = 2
        
        return {
            "task_type": task_type,
            "priority": priority,
            "confidence": confidence,
            "original_description": description,
            "processed_description": description.strip()
        }

def create_intelligent_task(description: str) -> Task:
    """Create a task with LLM interpretation"""
    interpreter = TaskInterpreter()
    interpretation = interpreter.interpret_task(description)
    
    task = Task(
        id=f"llm_task_{hash(description) % 10000}",
        description=interpretation["processed_description"],
        priority=interpretation["priority"]
    )
    
    # Add interpretation metadata
    task.metadata = interpretation
    
    return task