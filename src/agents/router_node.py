def route_query(query: str) -> str:
    query_lower = query.lower()
    weather_keywords = ["weather", "temperature", "forecast", "rain", "snow", "cold", "hot", "humid"]
    
    if any(keyword in query_lower for keyword in weather_keywords):
        return "weather"
    else:
        return "rag"


def router_node(state):
    user_input = state.get("user_input", "")
    
    if "weather" in user_input.lower() or "temperature" in user_input.lower():
        return {"route": "weather"}
    else:
        return {"route": "rag"}
