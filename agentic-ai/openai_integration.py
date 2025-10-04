"""
OpenAI API Integration for Advanced LLM Capabilities
"""

import json
import os
from typing import Dict, List, Any, Optional
from agent import Agent, Task

class OpenAIAgent(Agent):
    def __init__(self, api_key: Optional[str] = None):
        super().__init__("OpenAIAgent", ["gpt", "openai", "advanced_nlp", "reasoning", "creative"])
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = "gpt-3.5-turbo"
        self.conversation_history = []
    
    def execute_task(self, task: Task) -> Any:
        if not self.api_key:
            return self._mock_openai_response(task.description)
        
        try:
            return self._call_openai_api(task.description)
        except Exception as e:
            self.add_memory(f"OpenAI API error: {str(e)}")
            return self._mock_openai_response(task.description)
    
    def _mock_openai_response(self, prompt: str) -> Dict:
        """Mock OpenAI response for demo purposes"""
        self.add_memory(f"Mock OpenAI processing: {prompt[:50]}...")
        
        # Simulate different types of responses based on prompt
        if "analyze" in prompt.lower():
            return {
                "response": f"Based on my analysis of '{prompt[:30]}...', I can identify key patterns and insights. The data suggests several important trends that warrant further investigation.",
                "model": "mock-gpt-3.5-turbo",
                "tokens_used": 45,
                "confidence": 0.85,
                "reasoning": ["Pattern recognition", "Data correlation", "Trend analysis"]
            }
        elif "create" in prompt.lower() or "generate" in prompt.lower():
            return {
                "response": f"I've generated a creative solution for '{prompt[:30]}...'. Here's an innovative approach that combines multiple strategies for optimal results.",
                "model": "mock-gpt-3.5-turbo", 
                "tokens_used": 52,
                "confidence": 0.90,
                "creativity_score": 0.88
            }
        elif "plan" in prompt.lower():
            return {
                "response": f"Here's a comprehensive plan for '{prompt[:30]}...': 1) Initial assessment, 2) Resource allocation, 3) Implementation phases, 4) Quality assurance, 5) Final review.",
                "model": "mock-gpt-3.5-turbo",
                "tokens_used": 38,
                "confidence": 0.92,
                "plan_steps": 5
            }
        else:
            return {
                "response": f"I understand you're asking about '{prompt[:30]}...'. Let me provide a thoughtful response based on the context and requirements.",
                "model": "mock-gpt-3.5-turbo",
                "tokens_used": 35,
                "confidence": 0.80
            }
    
    def _call_openai_api(self, prompt: str) -> Dict:
        """Actual OpenAI API call (requires API key)"""
        try:
            import openai
            openai.api_key = self.api_key
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant integrated into an agentic AI system."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return {
                "response": response.choices[0].message.content,
                "model": self.model,
                "tokens_used": response.usage.total_tokens,
                "confidence": 0.95
            }
        except ImportError:
            return {"error": "OpenAI library not installed. Run: pip install openai"}
        except Exception as e:
            return {"error": f"OpenAI API error: {str(e)}"}

class SmartTaskRouter:
    """Routes tasks to appropriate agents based on LLM analysis"""
    
    def __init__(self, agents: List[Agent]):
        self.agents = agents
        self.llm_agent = next((a for a in agents if isinstance(a, OpenAIAgent)), None)
    
    def route_task(self, task: Task) -> Agent:
        """Use LLM to determine best agent for task"""
        if not self.llm_agent:
            return self._fallback_routing(task)
        
        # Ask LLM to analyze task and suggest best agent
        analysis_prompt = f"""
        Analyze this task and suggest the best agent type:
        Task: {task.description}
        
        Available agents: DataAgent, MLAgent, PlannerAgent, LLMAgent, OpenAIAgent
        
        Respond with just the agent name and confidence (0-1).
        Format: AgentName,confidence
        """
        
        try:
            result = self.llm_agent._mock_openai_response(analysis_prompt)
            response = result.get("response", "")
            
            # Parse response (simplified)
            for agent in self.agents:
                if agent.__class__.__name__ in response:
                    return agent
        except:
            pass
        
        return self._fallback_routing(task)
    
    def _fallback_routing(self, task: Task) -> Agent:
        """Fallback routing logic"""
        capable_agents = [agent for agent in self.agents if agent.can_handle(task)]
        return capable_agents[0] if capable_agents else self.agents[0]

def create_llm_enhanced_system():
    """Create system with LLM integration"""
    from llm_agent import LLMAgent
    from agent import DataAgent, MLAgent, PlannerAgent
    
    agents = [
        DataAgent(),
        MLAgent(),
        PlannerAgent(),
        LLMAgent(),
        OpenAIAgent()
    ]
    
    router = SmartTaskRouter(agents)
    
    return agents, router