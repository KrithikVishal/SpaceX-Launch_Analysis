from google.adk.agents import Agent
from typing import Dict, List
import json

class PlannerAgent:
    def __init__(self):
        self.agent = Agent(
            name="planner_agent",
            description="Coordinates between agents to achieve user goals",
            tools=[self.create_plan]
        )
    
    def create_plan(self, goal: str) -> Dict:
        """
        Creates a plan to achieve the user's goal by coordinating between agents.
        Args:
            goal: The user's goal (e.g., "Find the next SpaceX launch, check weather, and assess delay probability")
        Returns:
            Dict containing the execution plan
        """
        # Parse the goal into steps
        steps = self._parse_goal(goal)
        
        # Create execution plan
        plan = {
            "goal": goal,
            "steps": steps,
            "current_step": 0,
            "status": "pending",
            "results": {}
        }
        
        return plan
    
    def _parse_goal(self, goal: str) -> List[Dict]:
        """
        Parses the user's goal into executable steps.
        """
        steps = []
        
        # Check for SpaceX launch related queries
        if "spacex" in goal.lower() or "launch" in goal.lower():
            steps.append({
                "agent": "spacex_agent",
                "action": "get_spacex_launch_info",
                "description": "Get information about the next SpaceX launch"
            })
        
        # Check for weather related queries
        if "weather" in goal.lower():
            steps.append({
                "agent": "weather_agent",
                "action": "get_forecast",
                "description": "Get weather forecast for launch location",
                "depends_on": ["spacex_agent"]  # Needs location from SpaceX agent
            })
        
        # Always include summarization if multiple steps are involved
        if len(steps) > 1:
            steps.append({
                "agent": "summarize_agent",
                "action": "create_launch_summary",
                "description": "Create comprehensive summary of launch and conditions",
                "depends_on": ["spacex_agent", "weather_agent"]
            })
        
        return steps
    
    def execute_plan(self, plan: Dict) -> Dict:
        """
        Executes the plan by coordinating between agents.
        """
        results = {}
        for step in plan["steps"]:
            # Check dependencies
            if "depends_on" in step:
                for dep in step["depends_on"]:
                    if dep not in results:
                        return {
                            "status": "error",
                            "message": f"Missing dependency: {dep}"
                        }
            
            # Execute step
            agent_name = step["agent"]
            action = step["action"]
            
            # Get agent instance and execute action
            agent = self._get_agent(agent_name)
            if not agent:
                return {
                    "status": "error",
                    "message": f"Agent not found: {agent_name}"
                }
            
            result = agent.execute(action, results)
            results[agent_name] = result
            
            if result.get("status") == "error":
                return {
                    "status": "error",
                    "message": f"Error in {agent_name}: {result.get('message')}",
                    "results": results
                }
        
        return {
            "status": "success",
            "results": results
        }
    
    def _get_agent(self, agent_name: str):
        """
        Gets the appropriate agent instance based on name.
        """
        if agent_name == "spacex_agent":
            from agents.spacex_agent import spacex_agent
            return spacex_agent
        elif agent_name == "weather_agent":
            from agents.weather_agent import weather_agent
            return weather_agent
        elif agent_name == "summarize_agent":
            from agents.summarize_agent import summarize_agent
            return summarize_agent
        return None

# Create the planner agent instance
planner_agent = PlannerAgent() 