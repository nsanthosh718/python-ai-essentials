"""
Demo: LLM-Enhanced Agentic AI System
"""

from coordinator import AgentCoordinator
from llm_agent import LLMAgent, TaskInterpreter, create_intelligent_task
from openai_integration import OpenAIAgent, SmartTaskRouter
from agent import DataAgent, MLAgent, PlannerAgent
import json

def main():
    print("🧠 Starting LLM-Enhanced Agentic AI System...")
    
    # Create enhanced system with LLM agents
    coordinator = AgentCoordinator()
    coordinator.agents.extend([
        LLMAgent(),
        OpenAIAgent()
    ])
    
    # Create task interpreter
    interpreter = TaskInterpreter()
    
    # Natural language task examples
    natural_tasks = [
        "Please analyze the customer feedback data and summarize key insights",
        "I need urgent help training a machine learning model for sales prediction",
        "Can you create a project plan for our new AI initiative?",
        "Summarize this text: The quarterly results show significant growth in revenue",
        "What's the sentiment of this review: This product is absolutely amazing!",
        "Help me understand what entities are in this text: Contact John at john@email.com or 555-123-4567"
    ]
    
    print("\n📝 Processing Natural Language Tasks...")
    
    for i, task_desc in enumerate(natural_tasks, 1):
        print(f"\n--- Task {i} ---")
        print(f"Input: {task_desc}")
        
        # Interpret the task
        interpretation = interpreter.interpret_task(task_desc)
        print(f"Interpreted as: {interpretation['task_type']} (confidence: {interpretation['confidence']})")
        print(f"Priority: {interpretation['priority']}")
        
        # Create and execute task
        task = create_intelligent_task(task_desc)
        coordinator.task_queue.append(task)
        
        # Execute the task
        result = coordinator.execute_next_task()
        
        if result["status"] == "success":
            print(f"✅ Executed by: {result['agent']}")
            print(f"Result: {json.dumps(result['result'], indent=2)}")
        else:
            print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    print("\n📊 System Performance Summary:")
    status = coordinator.get_system_status()
    print(f"Total agents: {len(status['agents'])}")
    print(f"Completed tasks: {status['completed_tasks']}")
    
    print("\n🧠 LLM Agent Memory:")
    llm_agent = next((a for a in coordinator.agents if a.name == "LLMAgent"), None)
    if llm_agent and llm_agent.memory:
        for memory in llm_agent.memory[-3:]:  # Show last 3 memories
            print(f"  - {memory['info']}")

def interactive_mode():
    """Interactive mode for testing LLM integration"""
    print("\n🎯 Interactive LLM Mode (type 'quit' to exit)")
    
    coordinator = AgentCoordinator()
    coordinator.agents.extend([LLMAgent(), OpenAIAgent()])
    
    while True:
        user_input = input("\n💬 Enter a task: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        
        if not user_input:
            continue
        
        # Process the natural language input
        task = create_intelligent_task(user_input)
        coordinator.task_queue.append(task)
        
        result = coordinator.execute_next_task()
        
        if result["status"] == "success":
            print(f"🤖 {result['agent']}: {result['result'].get('response', result['result'])}")
        else:
            print(f"❌ Error: {result.get('error', 'Task failed')}")

if __name__ == "__main__":
    main()
    
    # Uncomment for interactive mode
    # interactive_mode()