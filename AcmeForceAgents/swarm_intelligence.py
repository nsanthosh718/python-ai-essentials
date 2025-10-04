"""
AcmeForceAgents (AFA) - Swarm Intelligence System
Advanced multi-agent collaboration with emergent intelligence
"""

import asyncio
import numpy as np
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import networkx as nx
from collections import defaultdict, deque
import json
import time
from datetime import datetime
import random

class SwarmRole(Enum):
    LEADER = "leader"
    SCOUT = "scout"
    WORKER = "worker"
    SPECIALIST = "specialist"
    COORDINATOR = "coordinator"
    INNOVATOR = "innovator"

class CommunicationProtocol(Enum):
    BROADCAST = "broadcast"
    DIRECT = "direct"
    MULTICAST = "multicast"
    CONSENSUS = "consensus"
    AUCTION = "auction"
    NEGOTIATION = "negotiation"

@dataclass
class SwarmMessage:
    sender_id: str
    receiver_id: Optional[str]
    message_type: str
    content: Dict
    timestamp: datetime
    priority: int = 1
    ttl: int = 10  # Time to live
    protocol: CommunicationProtocol = CommunicationProtocol.DIRECT

@dataclass
class SwarmTask:
    task_id: str
    description: str
    requirements: Dict
    complexity: float
    deadline: Optional[datetime]
    assigned_agents: Set[str] = field(default_factory=set)
    status: str = "pending"
    result: Optional[Dict] = None

class SwarmIntelligence:
    def __init__(self, max_agents: int = 100):
        self.agents = {}
        self.communication_network = nx.DiGraph()
        self.task_queue = deque()
        self.completed_tasks = []
        self.message_bus = MessageBus()
        self.consensus_engine = ConsensusEngine()
        self.emergence_detector = EmergenceDetector()
        
        # Swarm metrics
        self.swarm_metrics = {
            'collective_intelligence': 0.0,
            'coordination_efficiency': 0.0,
            'task_completion_rate': 0.0,
            'emergence_events': 0,
            'network_density': 0.0
        }
        
        # Dynamic role assignment
        self.role_manager = DynamicRoleManager()
        self.load_balancer = SwarmLoadBalancer()
        
    async def add_agent(self, agent):
        """Add agent to swarm with dynamic role assignment"""
        self.agents[agent.agent_id] = agent
        self.communication_network.add_node(agent.agent_id)
        
        # Assign initial role based on capabilities
        role = await self.role_manager.assign_role(agent, self.agents)
        agent.swarm_role = role
        
        # Establish communication links
        await self._establish_communication_links(agent)
        
        # Update swarm metrics
        self._update_swarm_metrics()
        
        return role
    
    async def _establish_communication_links(self, new_agent):
        """Establish optimal communication links for new agent"""
        # Connect to similar agents
        for agent_id, agent in self.agents.items():
            if agent_id != new_agent.agent_id:
                similarity = self._calculate_agent_similarity(new_agent, agent)
                if similarity > 0.7:  # High similarity threshold
                    self.communication_network.add_edge(new_agent.agent_id, agent_id, weight=similarity)
                    self.communication_network.add_edge(agent_id, new_agent.agent_id, weight=similarity)
        
        # Ensure network connectivity
        if self.communication_network.number_of_nodes() > 1:
            if not nx.is_connected(self.communication_network.to_undirected()):
                # Connect to highest degree node to ensure connectivity
                degrees = dict(self.communication_network.degree())
                hub_agent = max(degrees, key=degrees.get)
                self.communication_network.add_edge(new_agent.agent_id, hub_agent, weight=0.5)
                self.communication_network.add_edge(hub_agent, new_agent.agent_id, weight=0.5)
    
    def _calculate_agent_similarity(self, agent1, agent2):
        """Calculate similarity between two agents"""
        # Compare specializations
        spec_similarity = 1.0 if agent1.specialization == agent2.specialization else 0.3
        
        # Compare performance metrics
        perf_similarity = 1.0 - np.mean([
            abs(agent1.performance_metrics[key] - agent2.performance_metrics[key])
            for key in agent1.performance_metrics.keys()
            if key in agent2.performance_metrics
        ])
        
        return 0.6 * spec_similarity + 0.4 * perf_similarity
    
    async def execute_swarm_task(self, task: SwarmTask):
        """Execute task using swarm intelligence"""
        # Task decomposition
        subtasks = await self._decompose_task(task)
        
        # Agent selection and assignment
        assigned_agents = await self._select_optimal_agents(subtasks)
        
        # Coordinate execution
        results = await self._coordinate_execution(subtasks, assigned_agents)
        
        # Aggregate results
        final_result = await self._aggregate_results(results, task)
        
        # Learn from execution
        await self._learn_from_swarm_execution(task, final_result)
        
        return final_result
    
    async def _decompose_task(self, task: SwarmTask) -> List[Dict]:
        """Intelligently decompose complex task into subtasks"""
        complexity = task.complexity
        
        if complexity < 0.3:
            # Simple task - no decomposition needed
            return [{'subtask_id': f"{task.task_id}_0", 'description': task.description, 'requirements': task.requirements}]
        
        elif complexity < 0.7:
            # Medium complexity - split into 2-3 subtasks
            return [
                {'subtask_id': f"{task.task_id}_1", 'description': f"Phase 1: {task.description}", 'requirements': task.requirements},
                {'subtask_id': f"{task.task_id}_2", 'description': f"Phase 2: {task.description}", 'requirements': task.requirements}
            ]
        
        else:
            # High complexity - split into multiple specialized subtasks
            return [
                {'subtask_id': f"{task.task_id}_data", 'description': f"Data processing: {task.description}", 'requirements': {'specialization': 'data'}},
                {'subtask_id': f"{task.task_id}_analysis", 'description': f"Analysis: {task.description}", 'requirements': {'specialization': 'analysis'}},
                {'subtask_id': f"{task.task_id}_synthesis", 'description': f"Synthesis: {task.description}", 'requirements': {'specialization': 'general'}},
                {'subtask_id': f"{task.task_id}_validation", 'description': f"Validation: {task.description}", 'requirements': {'specialization': 'validation'}}
            ]
    
    async def _select_optimal_agents(self, subtasks: List[Dict]) -> Dict[str, str]:
        """Select optimal agents for each subtask using auction mechanism"""
        assignments = {}
        
        for subtask in subtasks:
            # Broadcast task to all agents
            bids = await self._conduct_task_auction(subtask)
            
            # Select best bid
            if bids:
                best_agent = min(bids, key=lambda x: bids[x]['cost'])
                assignments[subtask['subtask_id']] = best_agent
        
        return assignments
    
    async def _conduct_task_auction(self, subtask: Dict) -> Dict[str, Dict]:
        """Conduct auction for subtask assignment"""
        bids = {}
        
        for agent_id, agent in self.agents.items():
            # Calculate agent's bid based on capability and current load
            capability_score = self._calculate_capability_score(agent, subtask['requirements'])
            current_load = len(agent.autonomous_goals)  # Simplified load metric
            
            if capability_score > 0.5:  # Only bid if capable
                cost = (1.0 - capability_score) + (current_load * 0.1)
                confidence = capability_score * (1.0 - current_load * 0.05)
                
                bids[agent_id] = {
                    'cost': cost,
                    'confidence': confidence,
                    'estimated_time': random.uniform(1.0, 10.0)  # Simplified
                }
        
        return bids
    
    def _calculate_capability_score(self, agent, requirements: Dict) -> float:
        """Calculate how well an agent matches task requirements"""
        score = 0.5  # Base score
        
        # Specialization match
        if 'specialization' in requirements:
            if agent.specialization == requirements['specialization']:
                score += 0.3
            elif agent.specialization == 'general':
                score += 0.1
        
        # Performance metrics
        score += agent.performance_metrics.get('accuracy', 0.5) * 0.2
        
        return min(score, 1.0)
    
    async def _coordinate_execution(self, subtasks: List[Dict], assignments: Dict[str, str]) -> Dict[str, Dict]:
        """Coordinate parallel execution of subtasks"""
        execution_tasks = []
        
        for subtask in subtasks:
            subtask_id = subtask['subtask_id']
            if subtask_id in assignments:
                agent_id = assignments[subtask_id]
                agent = self.agents[agent_id]
                
                # Create execution coroutine
                task_coro = self._execute_subtask(agent, subtask)
                execution_tasks.append((subtask_id, task_coro))
        
        # Execute all subtasks concurrently
        results = {}
        completed_tasks = await asyncio.gather(*[task for _, task in execution_tasks], return_exceptions=True)
        
        for i, (subtask_id, _) in enumerate(execution_tasks):
            if isinstance(completed_tasks[i], Exception):
                results[subtask_id] = {'error': str(completed_tasks[i]), 'success': False}
            else:
                results[subtask_id] = completed_tasks[i]
        
        return results
    
    async def _execute_subtask(self, agent, subtask: Dict) -> Dict:
        """Execute a single subtask with an agent"""
        start_time = time.time()
        
        try:
            # Simulate task execution
            await asyncio.sleep(random.uniform(0.1, 1.0))  # Simulated work
            
            result = {
                'subtask_id': subtask['subtask_id'],
                'agent_id': agent.agent_id,
                'success': True,
                'execution_time': time.time() - start_time,
                'result_data': f"Completed: {subtask['description']}",
                'confidence': random.uniform(0.7, 0.95)
            }
            
            # Update agent performance
            agent.performance_metrics['accuracy'] = 0.9 * agent.performance_metrics['accuracy'] + 0.1 * result['confidence']
            
            return result
            
        except Exception as e:
            return {
                'subtask_id': subtask['subtask_id'],
                'agent_id': agent.agent_id,
                'success': False,
                'error': str(e),
                'execution_time': time.time() - start_time
            }
    
    async def _aggregate_results(self, results: Dict[str, Dict], original_task: SwarmTask) -> Dict:
        """Aggregate subtask results into final result"""
        successful_results = [r for r in results.values() if r.get('success', False)]
        failed_results = [r for r in results.values() if not r.get('success', False)]
        
        overall_success = len(successful_results) > len(failed_results)
        
        aggregated_result = {
            'task_id': original_task.task_id,
            'success': overall_success,
            'subtask_results': results,
            'successful_subtasks': len(successful_results),
            'failed_subtasks': len(failed_results),
            'total_execution_time': sum(r.get('execution_time', 0) for r in results.values()),
            'average_confidence': np.mean([r.get('confidence', 0.5) for r in successful_results]) if successful_results else 0.0,
            'participating_agents': list(set(r.get('agent_id') for r in results.values() if r.get('agent_id'))),
            'completion_timestamp': datetime.now()
        }
        
        return aggregated_result
    
    async def _learn_from_swarm_execution(self, task: SwarmTask, result: Dict):
        """Learn from swarm execution to improve future performance"""
        # Update swarm metrics
        self.swarm_metrics['task_completion_rate'] = (
            0.9 * self.swarm_metrics['task_completion_rate'] + 
            0.1 * (1.0 if result['success'] else 0.0)
        )
        
        # Update coordination efficiency
        expected_time = task.complexity * 5.0  # Simplified expectation
        actual_time = result['total_execution_time']
        efficiency = min(expected_time / max(actual_time, 0.1), 1.0)
        
        self.swarm_metrics['coordination_efficiency'] = (
            0.9 * self.swarm_metrics['coordination_efficiency'] + 
            0.1 * efficiency
        )
        
        # Detect emergent behaviors
        emergence_detected = await self.emergence_detector.detect_emergence(result, self.agents)
        if emergence_detected:
            self.swarm_metrics['emergence_events'] += 1
    
    def _update_swarm_metrics(self):
        """Update overall swarm intelligence metrics"""
        if not self.agents:
            return
        
        # Calculate collective intelligence
        individual_intelligences = [
            np.mean(list(agent.performance_metrics.values()))
            for agent in self.agents.values()
        ]
        
        self.swarm_metrics['collective_intelligence'] = np.mean(individual_intelligences)
        
        # Calculate network density
        if self.communication_network.number_of_nodes() > 1:
            self.swarm_metrics['network_density'] = nx.density(self.communication_network)
    
    async def evolve_swarm_structure(self):
        """Evolve the swarm's communication structure and roles"""
        # Analyze current performance
        current_performance = self.swarm_metrics['collective_intelligence']
        
        # Try different network topologies
        if current_performance < 0.7:
            await self._restructure_communication_network()
        
        # Reassign roles based on performance
        await self.role_manager.reassign_roles(self.agents)
        
        # Optimize load distribution
        await self.load_balancer.rebalance_load(self.agents)

class MessageBus:
    def __init__(self):
        self.message_queue = asyncio.Queue()
        self.subscribers = defaultdict(list)
        self.message_history = deque(maxlen=10000)
    
    async def publish(self, message: SwarmMessage):
        """Publish message to the bus"""
        await self.message_queue.put(message)
        self.message_history.append(message)
    
    async def subscribe(self, agent_id: str, message_types: List[str]):
        """Subscribe agent to specific message types"""
        for msg_type in message_types:
            self.subscribers[msg_type].append(agent_id)
    
    async def process_messages(self):
        """Process messages in the queue"""
        while True:
            try:
                message = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
                await self._route_message(message)
            except asyncio.TimeoutError:
                continue
    
    async def _route_message(self, message: SwarmMessage):
        """Route message to appropriate recipients"""
        if message.protocol == CommunicationProtocol.BROADCAST:
            # Send to all subscribers
            recipients = self.subscribers.get(message.message_type, [])
            for recipient in recipients:
                await self._deliver_message(message, recipient)
        elif message.protocol == CommunicationProtocol.DIRECT:
            # Send to specific recipient
            if message.receiver_id:
                await self._deliver_message(message, message.receiver_id)
    
    async def _deliver_message(self, message: SwarmMessage, recipient_id: str):
        """Deliver message to specific recipient"""
        # Implementation would depend on agent communication interface
        pass

class ConsensusEngine:
    def __init__(self):
        self.consensus_threshold = 0.67  # 2/3 majority
        self.active_proposals = {}
    
    async def propose_consensus(self, proposal_id: str, proposal_data: Dict, participating_agents: List[str]):
        """Initiate consensus process"""
        self.active_proposals[proposal_id] = {
            'data': proposal_data,
            'participants': participating_agents,
            'votes': {},
            'status': 'active',
            'created_at': datetime.now()
        }
        
        # Broadcast proposal to participants
        # Implementation would send proposal to all participating agents
        
        return proposal_id
    
    async def cast_vote(self, proposal_id: str, agent_id: str, vote: bool, confidence: float):
        """Cast vote for a proposal"""
        if proposal_id in self.active_proposals:
            proposal = self.active_proposals[proposal_id]
            proposal['votes'][agent_id] = {'vote': vote, 'confidence': confidence}
            
            # Check if consensus reached
            if len(proposal['votes']) >= len(proposal['participants']) * self.consensus_threshold:
                consensus_result = await self._evaluate_consensus(proposal_id)
                return consensus_result
        
        return None
    
    async def _evaluate_consensus(self, proposal_id: str):
        """Evaluate if consensus has been reached"""
        proposal = self.active_proposals[proposal_id]
        votes = proposal['votes']
        
        # Weighted voting based on confidence
        total_weight = sum(vote_data['confidence'] for vote_data in votes.values())
        positive_weight = sum(
            vote_data['confidence'] for vote_data in votes.values() 
            if vote_data['vote']
        )
        
        consensus_ratio = positive_weight / total_weight if total_weight > 0 else 0
        
        consensus_reached = consensus_ratio >= self.consensus_threshold
        
        proposal['status'] = 'consensus_reached' if consensus_reached else 'consensus_failed'
        proposal['consensus_ratio'] = consensus_ratio
        
        return {
            'proposal_id': proposal_id,
            'consensus_reached': consensus_reached,
            'consensus_ratio': consensus_ratio,
            'participating_votes': len(votes)
        }

class EmergenceDetector:
    def __init__(self):
        self.emergence_patterns = []
        self.baseline_metrics = {}
    
    async def detect_emergence(self, execution_result: Dict, agents: Dict) -> bool:
        """Detect emergent behaviors in swarm execution"""
        # Look for unexpected performance improvements
        if execution_result.get('average_confidence', 0) > 0.9:
            # Check if this is significantly better than individual agent performance
            individual_avg = np.mean([
                np.mean(list(agent.performance_metrics.values()))
                for agent in agents.values()
            ])
            
            if execution_result['average_confidence'] > individual_avg * 1.2:
                self.emergence_patterns.append({
                    'type': 'performance_emergence',
                    'improvement_factor': execution_result['average_confidence'] / individual_avg,
                    'timestamp': datetime.now(),
                    'participating_agents': execution_result.get('participating_agents', [])
                })
                return True
        
        return False

class DynamicRoleManager:
    def __init__(self):
        self.role_assignments = {}
        self.role_performance = defaultdict(list)
    
    async def assign_role(self, agent, existing_agents: Dict) -> SwarmRole:
        """Assign optimal role to agent based on capabilities and swarm needs"""
        # Analyze current role distribution
        current_roles = [a.swarm_role for a in existing_agents.values() if hasattr(a, 'swarm_role')]
        role_counts = {role: current_roles.count(role) for role in SwarmRole}
        
        # Determine agent's best fit
        agent_capabilities = self._analyze_agent_capabilities(agent)
        
        # Assign role based on capabilities and swarm needs
        if agent_capabilities['leadership'] > 0.8 and role_counts.get(SwarmRole.LEADER, 0) < 2:
            return SwarmRole.LEADER
        elif agent_capabilities['innovation'] > 0.8:
            return SwarmRole.INNOVATOR
        elif agent_capabilities['specialization'] > 0.8:
            return SwarmRole.SPECIALIST
        elif agent_capabilities['coordination'] > 0.7:
            return SwarmRole.COORDINATOR
        else:
            return SwarmRole.WORKER
    
    def _analyze_agent_capabilities(self, agent) -> Dict[str, float]:
        """Analyze agent's capabilities for role assignment"""
        return {
            'leadership': agent.performance_metrics.get('collaboration_score', 0.5),
            'innovation': random.uniform(0.3, 0.9),  # Simplified
            'specialization': 0.9 if agent.specialization != 'general' else 0.3,
            'coordination': agent.performance_metrics.get('accuracy', 0.5)
        }
    
    async def reassign_roles(self, agents: Dict):
        """Reassign roles based on performance"""
        for agent_id, agent in agents.items():
            current_performance = np.mean(list(agent.performance_metrics.values()))
            
            # Consider role change if performance is suboptimal
            if current_performance < 0.6:
                new_role = await self.assign_role(agent, agents)
                if new_role != agent.swarm_role:
                    agent.swarm_role = new_role

class SwarmLoadBalancer:
    def __init__(self):
        self.load_history = defaultdict(list)
    
    async def rebalance_load(self, agents: Dict):
        """Rebalance workload across agents"""
        # Calculate current loads
        agent_loads = {
            agent_id: len(agent.autonomous_goals)
            for agent_id, agent in agents.items()
        }
        
        # Identify overloaded and underloaded agents
        avg_load = np.mean(list(agent_loads.values())) if agent_loads else 0
        
        overloaded = [aid for aid, load in agent_loads.items() if load > avg_load * 1.5]
        underloaded = [aid for aid, load in agent_loads.items() if load < avg_load * 0.5]
        
        # Redistribute tasks
        for overloaded_agent_id in overloaded:
            if underloaded:
                # Move some tasks to underloaded agents
                target_agent_id = random.choice(underloaded)
                await self._transfer_tasks(overloaded_agent_id, target_agent_id, agents)
    
    async def _transfer_tasks(self, from_agent_id: str, to_agent_id: str, agents: Dict):
        """Transfer tasks between agents"""
        from_agent = agents[from_agent_id]
        to_agent = agents[to_agent_id]
        
        # Transfer one task (simplified)
        if from_agent.autonomous_goals:
            task = from_agent.autonomous_goals.pop()
            to_agent.autonomous_goals.append(task)