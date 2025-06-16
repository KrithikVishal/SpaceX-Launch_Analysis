import requests
from datetime import datetime
from google.adk.agents import Agent
from typing import Dict

# Constants
VISUAL_CROSSING_API_KEY = "V6VD25NGRVEH7U9X4KR4K9PAW"
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

def validate_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def get_weather_forecast(city: str, date: str) -> Dict:
    """
    Get weather forecast for a specific city and date.
    Args:
        city: City name (e.g., "Cape Canaveral, FL")
        date: Date in YYYY-MM-DD format
    Returns:
        Dict containing weather forecast data
    """
    if not validate_date(date):
        return {"status": "error", "message": "Invalid date format. Use YYYY-MM-DD."}
    
    url = f"{BASE_URL}/{city}/{date}"
    params = {
        "key": VISUAL_CROSSING_API_KEY,
        "unitGroup": "metric",
        "include": "days",
        "contentType": "json"
    }
    
    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        day = resp.json().get("days", [{}])[0]
        
        return {
            "status": "success",
            "data": {
                "temp_min": day.get("tempmin"),
                "temp_max": day.get("tempmax"),
                "wind_speed": day.get("windspeed"),
                "cloud_cover": day.get("cloudcover"),
                "precip": day.get("precip"),
                "visibility": day.get("visibility"),
                "conditions": day.get("conditions", "")
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def assess_launch_conditions(data: Dict) -> Dict:
    """
    Assess weather conditions for a rocket launch.
    Args:
        data: Weather data dictionary
    Returns:
        Dict containing assessment results
    """
    issues = []
    recommendations = []
    
    # Temperature assessment
    if data["temp_min"] < 4:
        issues.append("Temperature too low for launch")
        recommendations.append("Consider delaying until temperatures rise")
    elif data["temp_max"] > 37:
        issues.append("Temperature too high for launch")
        recommendations.append("Consider early morning or evening launch")
    
    # Wind assessment
    if data["wind_speed"] > 56:
        issues.append("Wind speed too high for launch")
        recommendations.append("Wait for wind conditions to improve")
    elif data["wind_speed"] > 30:
        issues.append("Elevated wind speeds")
        recommendations.append("Monitor wind conditions closely")
    
    # Cloud cover assessment
    if data["cloud_cover"] > 50:
        issues.append("High cloud cover")
        recommendations.append("Consider visibility impact on launch")
    
    # Precipitation assessment
    if data["precip"] > 0:
        issues.append("Precipitation expected")
        recommendations.append("Delay launch until precipitation clears")
    
    # Visibility assessment
    if data["visibility"] < 8:
        issues.append("Low visibility conditions")
        recommendations.append("Wait for visibility to improve")
    
    # Determine risk level and launch advisability
    risk_level = "high" if len(issues) > 2 else "medium" if len(issues) > 0 else "low"
    launch_advisable = len(issues) == 0
    
    return {
        "status": "success",
        "data": {
            "issues": issues,
            "recommendations": recommendations,
            "launch_advisable": launch_advisable,
            "risk_level": risk_level
        }
    }

def analyze_weather(city: str, date: str) -> Dict:
    """
    Analyze weather conditions for a launch.
    Args:
        city: City name
        date: Date in YYYY-MM-DD format
    Returns:
        Dict containing weather analysis results
    """
    try:
        if not city or not date:
            return {
                "status": "error",
                "message": "Missing required parameters: city and date"
            }
        
        forecast = get_weather_forecast(city, date)
        if forecast["status"] == "error":
            return forecast
        
        assessment = assess_launch_conditions(forecast["data"])
        
        # Create detailed weather summary
        weather_summary = f"""
Weather Analysis for {city} on {date}:

Current Conditions:
- Temperature Range: {forecast['data']['temp_min']}°C to {forecast['data']['temp_max']}°C
- Wind Speed: {forecast['data']['wind_speed']} km/h
- Cloud Cover: {forecast['data']['cloud_cover']}%
- Precipitation: {forecast['data']['precip']} mm
- Visibility: {forecast['data']['visibility']} km
- Conditions: {forecast['data']['conditions']}

Launch Assessment:
- Risk Level: {assessment['data']['risk_level'].upper()}
- Launch Advisable: {'Yes' if assessment['data']['launch_advisable'] else 'No'}

"""
        if assessment['data']['issues']:
            weather_summary += "\nIssues Identified:\n"
            for issue in assessment['data']['issues']:
                weather_summary += f"- {issue}\n"
        
        if assessment['data']['recommendations']:
            weather_summary += "\nRecommendations:\n"
            for rec in assessment['data']['recommendations']:
                weather_summary += f"- {rec}\n"
        
        return {
            "status": "success",
            "data": {
                "forecast": forecast["data"],
                "assessment": assessment["data"],
                "summary": weather_summary.strip()
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Create the weather agent
weather_agent = Agent(
    name="weather_agent",
    description="Agent that provides weather forecasts and launch condition assessments",
    tools=[analyze_weather]
)

if __name__ == "__main__":
    city = "Cape Canaveral, FL"
    date = datetime.today().strftime("%Y-%m-%d")

    forecast = get_weather_forecast(city, date)
    if "status" in forecast and forecast["status"] == "error":
        print(f"❌ Error: {forecast['message']}")
    else:
        print(f"🌤️ Weather Forecast for {city} on {date}:")
        print(f"- Min Temp: {forecast['data']['temp_min']}°C")
        print(f"- Max Temp: {forecast['data']['temp_max']}°C")
        print(f"- Wind Speed: {forecast['data']['wind_speed']} km/h")
        print(f"- Cloud Cover: {forecast['data']['cloud_cover']}%")
        print(f"- Precipitation: {forecast['data']['precip']} mm")
        print(f"- Visibility: {forecast['data']['visibility']} km")

        conditions = forecast['data']['conditions']
        if conditions:
            print(f"Conditions: {conditions}")

        assessment = assess_launch_conditions(forecast['data'])
        if assessment['data']['launch_advisable']:
            print("✅ Weather is suitable for a launch.")
        else:
            print("🚫 Launch not advised due to:")
            for c in assessment['data']['issues']:
                print(f" - {c}")