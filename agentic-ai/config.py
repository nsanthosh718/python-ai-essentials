"""
Configuration for LLM Integration
"""

import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class LLMConfig:
    # OpenAI Configuration
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"
    max_tokens: int = 150
    temperature: float = 0.7
    
    # Local LLM Configuration (for future integration)
    local_model_path: Optional[str] = None
    use_local_model: bool = False
    
    # Task Processing
    enable_smart_routing: bool = True
    enable_task_interpretation: bool = True
    
    def __post_init__(self):
        # Try to load API key from environment
        if not self.openai_api_key:
            self.openai_api_key = os.getenv("OPENAI_API_KEY")

# Global configuration instance
llm_config = LLMConfig()

def setup_llm_config(api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
    """Setup LLM configuration"""
    global llm_config
    if api_key:
        llm_config.openai_api_key = api_key
    llm_config.openai_model = model
    return llm_config