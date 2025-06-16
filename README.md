# Multi-Agent System for SpaceX Launch Analysis

This project implements a multi-agent system using Google's Agent Development Kit (ADK) that analyzes SpaceX launches and weather conditions to provide comprehensive launch assessments.

## Features

- **Planner Agent**: Coordinates between agents and creates execution plans
- **SpaceX Agent**: Fetches and analyzes SpaceX launch information using the Spaceflight News API
- **Weather Agent**: Provides weather forecasts and launch condition assessments using Visual Crossing Weather API

## Project Structure

```
.
├── agents/
│   ├── __init__.py
│   ├── planner_agent.py
│   ├── spacex_agent.py
│   └── weather_agent.py
├── requirements.txt
└── README.md
```

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your API keys and paste your API keys in the agent's python codes:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   VISUAL_CROSSING_API_KEY=your_visual_crossing_api_key
   ```

## Usage

The agents can be used independently or together:

1. **Planner Agent** (`planner_agent.py`):
   - Coordinates between other agents
   - Creates execution plans based on user goals

2. **SpaceX Agent** (`spacex_agent.py`):
   - Fetches launch information from Spaceflight News API
   - Extracts mission details
   - Identifies launch location

3. **Weather Agent** (`weather_agent.py`):
   - Gets weather forecast from Visual Crossing Weather API
   - Assesses launch conditions
   - Identifies potential issues

## API Dependencies

- Google Gemini API: For natural language processing and agent coordination
- Visual Crossing Weather API: For weather forecasts and conditions
- Spaceflight News API: For SpaceX launch information

## License

MIT License 