import requests
from google.adk.agents import Agent
from typing import Dict, List, Optional

# SNAPI base URL
SNAPI_BASE_URL = "https://api.spaceflightnewsapi.net/v4"
GEMINI_API_KEY = "AIzaSyDyhYPYqnU3y7LnMIvHKBF4J5RPLy17oic"

def get_latest_spacex_news(query: str = None) -> Dict:
    """
    Get latest SpaceX news from SNAPI.
    Args:
        query: Optional search query to filter news
    Returns:
        Dict containing news articles
    """
    try:
        url = f"{SNAPI_BASE_URL}/articles"
        params = {
            "limit": 10,
            "ordering": "-published_at"
        }
        if query:
            params["search"] = query
            
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def process_launch_info(articles: List[Dict]) -> Optional[Dict]:
    """
    Process articles to extract launch information.
    Args:
        articles: List of news articles from SNAPI
    Returns:
        Dict containing launch information or None if not found
    """
    try:
        for article in articles:
            if "launch" in article.get("title", "").lower() or "launch" in article.get("summary", "").lower():
                title = article.get("title", "")
                summary = article.get("summary", "")
                published_at = article.get("published_at", "")
                
                locations = ["Cape Canaveral", "Kennedy Space Center", "Vandenberg", "Starbase", "Boca Chica"]
                location = None
                for loc in locations:
                    if loc.lower() in (title + " " + summary).lower():
                        location = loc
                        break
                
                if location:
                    return {
                        "mission": title,
                        "date": published_at.split("T")[0],
                        "location": location,
                        "summary": summary,
                        "article_url": article.get("url", "")
                    }
        return None
    except Exception as e:
        return {"error": str(e)}

def get_spacex_launch_info(query: str) -> Dict:
    """
    Get SpaceX launch information based on user query.
    Args:
        query: User's query about SpaceX launches
    Returns:
        Dict containing launch information and related news
    """
    try:
        news_data = get_latest_spacex_news(query)
        
        if "error" in news_data:
            return {"status": "error", "message": news_data["error"]}
            
        articles = news_data.get("results", [])
        if not articles:
            return {"status": "error", "message": "No articles found"}
            
        launch_info = process_launch_info(articles)
        if not launch_info:
            return {"status": "error", "message": "No launch information found in articles"}
        
        # Create a formatted summary
        summary = f"""
Launch Information:
Mission: {launch_info['mission']}
Date: {launch_info['date']}
Location: {launch_info['location']}

Mission Summary:
{launch_info['summary']}

For more details, visit: {launch_info['article_url']}
"""
            
        return {
            "status": "success",
            "launch_info": launch_info,
            "summary": summary.strip(),
            "related_articles": articles[:3]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Create the SpaceX agent
spacex_agent = Agent(
    name="spacex_agent",
    description="Agent that fetches and analyzes SpaceX launch information",
    tools=[get_spacex_launch_info]
) 