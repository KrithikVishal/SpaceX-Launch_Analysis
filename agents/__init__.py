from .spacex_agent import get_spacex_launch_info
from .weather_agent import analyze_weather
from google.adk.agents import LlmAgent

# Root agent exposing both SpaceX and Weather tools
root_agent = LlmAgent(
    name="root_agent",
    description="Root agent for SpaceX news and Weather analysis.",
    tools=[get_spacex_launch_info, analyze_weather],
    model="gemini-1.5-flash"
)

__all__ = ['root_agent'] 