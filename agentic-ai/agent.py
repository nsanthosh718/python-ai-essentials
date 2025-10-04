"""
Core Agent Framework for Agentic AI System
"""

import json
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Any, Optional

@dataclass
class Task:
    id: str
    description: str
    priority: int = 1
    status: str = "pending"
    result: Optional[Any] = None

class Agent(ABC):
    def __init__(self, name: str, capabilities: List[str]):
        self.name = name
        self.capabilities = capabilities
        self.memory = []
        self.tasks = []
    
    @abstractmethod
    def execute_task(self, task: Task) -> Any:
        pass
    
    def can_handle(self, task: Task) -> bool:
        return any(cap in task.description.lower() for cap in self.capabilities)
    
    def add_memory(self, info: str):
        self.memory.append({"timestamp": time.time(), "info": info})
    
    def get_status(self) -> Dict:
        return {
            "name": self.name,
            "capabilities": self.capabilities,
            "active_tasks": len([t for t in self.tasks if t.status == "running"]),
            "completed_tasks": len([t for t in self.tasks if t.status == "completed"])
        }

class DataAgent(Agent):
    def __init__(self):
        super().__init__("DataAgent", ["data", "analysis", "processing", "csv", "json"])
    
    def execute_task(self, task: Task) -> Any:
        self.add_memory(f"Processing data task: {task.description}")
        
        if "analyze" in task.description.lower():
            return {"analysis": "Data processed", "records": 1000, "insights": ["trend_up", "outliers_detected"]}
        elif "clean" in task.description.lower():
            return {"cleaned_records": 950, "removed_duplicates": 50}
        else:
            return {"status": "data_processed", "timestamp": time.time()}

class MLAgent(Agent):
    def __init__(self):
        super().__init__("MLAgent", ["model", "train", "predict", "machine learning", "ml"])
    
    def execute_task(self, task: Task) -> Any:
        self.add_memory(f"Executing ML task: {task.description}")
        
        if "train" in task.description.lower():
            return {"model_accuracy": 0.92, "epochs": 100, "loss": 0.08}
        elif "predict" in task.description.lower():
            return {"predictions": [0.8, 0.6, 0.9], "confidence": 0.85}
        else:
            return {"model_status": "ready", "performance": "good"}

class PlannerAgent(Agent):
    def __init__(self):
        super().__init__("PlannerAgent", ["plan", "coordinate", "schedule", "organize"])
    
    def execute_task(self, task: Task) -> Any:
        self.add_memory(f"Planning task: {task.description}")
        
        # Break down complex tasks into subtasks
        if "project" in task.description.lower():
            return {
                "subtasks": [
                    "data_collection",
                    "data_analysis", 
                    "model_training",
                    "evaluation"
                ],
                "timeline": "2 weeks",
                "resources_needed": ["data", "compute"]
            }
        else:
            return {"plan": "task_scheduled", "priority": task.priority}