"""
Agentic AI System Demo
Run autonomous agents collaborating on tasks
"""

from coordinator import AgentCoordinator
import json

def main():
    print("🤖 Starting Agentic AI System...")
    
    # Initialize coordinator
    coordinator = AgentCoordinator()
    
    # Add sample tasks
    tasks = [
        ("Analyze customer data for trends", 3),
        ("Train ML model for prediction", 2),
        ("Plan data science project timeline", 1),
        ("Clean and preprocess dataset", 2),
        ("Generate predictions for new data", 1)
    ]
    
    print("\n📋 Adding tasks to queue...")
    for description, priority in tasks:
        task_id = coordinator.add_task(description, priority)
        print(f"  ✓ Added: {description} (Priority: {priority})")
    
    print(f"\n🔄 Running autonomous execution cycle...")
    results = coordinator.run_autonomous_cycle()
    
    print("\n📊 Execution Results:")
    for i, result in enumerate(results, 1):
        status_icon = "✅" if result["status"] == "success" else "❌"
        print(f"  {status_icon} Task {i}: {result['agent']} - {result['status']}")
        if result["status"] == "success":
            print(f"     Result: {json.dumps(result['result'], indent=6)}")
    
    print("\n🏥 System Status:")
    status = coordinator.get_system_status()
    print(json.dumps(status, indent=2))
    
    print("\n🎯 Agent Memory Samples:")
    for agent in coordinator.agents:
        if agent.memory:
            print(f"  {agent.name}: {agent.memory[-1]['info']}")

if __name__ == "__main__":
    main()