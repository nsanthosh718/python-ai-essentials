"""
Agent Coordinator - Orchestrates multi-agent collaboration
"""

from agent import Agent, Task, DataAgent, MLAgent, PlannerAgent
from typing import List, Dict
import time

class AgentCoordinator:
    def __init__(self):
        self.agents = [
            DataAgent(),
            MLAgent(), 
            PlannerAgent()
        ]
        self.task_queue = []
        self.completed_tasks = []
    
    def add_task(self, description: str, priority: int = 1) -> str:
        task_id = f"task_{len(self.task_queue) + 1}_{int(time.time())}"
        task = Task(id=task_id, description=description, priority=priority)
        self.task_queue.append(task)
        return task_id
    
    def find_best_agent(self, task: Task) -> Agent:
        capable_agents = [agent for agent in self.agents if agent.can_handle(task)]
        if not capable_agents:
            return self.agents[0]  # Default to first agent
        
        # Select agent with least active tasks
        return min(capable_agents, key=lambda a: len([t for t in a.tasks if t.status == "running"]))
    
    def execute_next_task(self) -> Dict:
        if not self.task_queue:
            return {"status": "no_tasks", "message": "No pending tasks"}
        
        # Sort by priority
        self.task_queue.sort(key=lambda t: t.priority, reverse=True)
        task = self.task_queue.pop(0)
        
        # Find best agent
        agent = self.find_best_agent(task)
        
        # Execute task
        task.status = "running"
        agent.tasks.append(task)
        
        try:
            result = agent.execute_task(task)
            task.result = result
            task.status = "completed"
            self.completed_tasks.append(task)
            
            return {
                "status": "success",
                "task_id": task.id,
                "agent": agent.name,
                "result": result
            }
        except Exception as e:
            task.status = "failed"
            return {
                "status": "error",
                "task_id": task.id,
                "agent": agent.name,
                "error": str(e)
            }
    
    def run_autonomous_cycle(self, max_tasks: int = 5) -> List[Dict]:
        results = []
        executed = 0
        
        while self.task_queue and executed < max_tasks:
            result = self.execute_next_task()
            results.append(result)
            executed += 1
            time.sleep(0.1)  # Small delay between tasks
        
        return results
    
    def get_system_status(self) -> Dict:
        return {
            "agents": [agent.get_status() for agent in self.agents],
            "pending_tasks": len(self.task_queue),
            "completed_tasks": len(self.completed_tasks),
            "system_health": "operational"
        }