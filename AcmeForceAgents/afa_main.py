"""
AcmeForceAgents (AFA) - Main System
Revolutionary autonomous AI agents that evolve and collaborate
"""

import asyncio
from core_evolution_engine import AutonomousAgent, AgentState
from swarm_intelligence import SwarmIntelligence, SwarmTask
from quantum_reasoning import QuantumReasoningEngine
import time
import json

class AcmeForceAgents:
    def __init__(self):
        self.swarm = SwarmIntelligence(max_agents=50)
        self.quantum_engine = QuantumReasoningEngine()
        self.active_agents = {}
        self.system_metrics = {
            'total_agents': 0,
            'active_tasks': 0,
            'evolution_events': 0,
            'quantum_reasoning_calls': 0
        }
    
    async def create_agent(self, specialization="general"):
        """Create new autonomous agent"""
        agent_id = f"afa_{len(self.active_agents)}_{int(time.time())}"
        agent = AutonomousAgent(agent_id, specialization)
        
        # Add to swarm
        role = await self.swarm.add_agent(agent)
        
        # Start autonomous execution
        asyncio.create_task(agent.autonomous_execution_loop())
        
        self.active_agents[agent_id] = agent
        self.system_metrics['total_agents'] += 1
        
        return agent_id, role
    
    async def execute_complex_task(self, task_description, complexity=0.5):
        """Execute complex task using swarm intelligence"""
        task = SwarmTask(
            task_id=f"task_{int(time.time())}",
            description=task_description,
            requirements={},
            complexity=complexity,
            deadline=None
        )
        
        result = await self.swarm.execute_swarm_task(task)
        self.system_metrics['active_tasks'] += 1
        
        return result
    
    async def quantum_analyze(self, problem, context=None):
        """Perform quantum reasoning analysis"""
        result = await self.quantum_engine.quantum_reasoning(
            problem, context or {}
        )
        self.system_metrics['quantum_reasoning_calls'] += 1
        return result
    
    def get_system_status(self):
        """Get current system status"""
        return {
            'metrics': self.system_metrics,
            'swarm_metrics': self.swarm.swarm_metrics,
            'active_agents': len(self.active_agents),
            'agent_states': {
                aid: agent.state.value 
                for aid, agent in self.active_agents.items()
            }
        }

async def demo_afa_system():
    """Demonstrate AcmeForceAgents capabilities"""
    afa = AcmeForceAgents()
    
    print("🚀 AcmeForceAgents (AFA) Demo Starting...")
    
    # Create specialized agents
    agents = []
    for spec in ["data", "analysis", "optimization", "general"]:
        agent_id, role = await afa.create_agent(spec)
        agents.append((agent_id, spec, role))
        print(f"✅ Created {spec} agent: {agent_id} with role {role.value}")
    
    await asyncio.sleep(1)  # Let agents initialize
    
    # Execute complex task
    print("\n🎯 Executing complex swarm task...")
    task_result = await afa.execute_complex_task(
        "Analyze market trends and optimize investment strategy", 
        complexity=0.8
    )
    print(f"✅ Task completed: {task_result['success']}")
    
    # Quantum reasoning
    print("\n🧠 Performing quantum reasoning...")
    quantum_result = await afa.quantum_analyze(
        "What is the optimal approach for AI agent coordination?",
        {"agents": len(agents), "complexity": 0.8}
    )
    print(f"✅ Quantum analysis confidence: {quantum_result['reasoning_result']['confidence_level']:.2f}")
    
    # System status
    print("\n📊 System Status:")
    status = afa.get_system_status()
    print(json.dumps(status, indent=2, default=str))
    
    return afa

if __name__ == "__main__":
    asyncio.run(demo_afa_system())