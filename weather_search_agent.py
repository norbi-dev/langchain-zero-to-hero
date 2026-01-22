from langchain_ollama import ChatOllama
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_agent
from langchain.tools import tool
import requests

# 1. Setup LLM
llm = ChatOllama(model="ministral-3:8b", temperature=0)


# 2. Setup Weather Tool
@tool
def get_weather(location: str) -> str:
    """Get current weather for a location. Returns temperature, conditions, and other weather data."""
    try:
        # Geocoding API to get coordinates
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json"
        geo_response = requests.get(geocode_url, timeout=10)
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return f"Could not find location: {location}"

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        name = geo_data["results"][0]["name"]
        country = geo_data["results"][0].get("country", "")

        # Weather API
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m&timezone=auto"
        weather_response = requests.get(weather_url, timeout=10)
        weather_data = weather_response.json()

        current = weather_data["current"]
        temp = current["temperature_2m"]
        feels_like = current["apparent_temperature"]
        humidity = current["relative_humidity_2m"]
        wind_speed = current["wind_speed_10m"]
        precip = current["precipitation"]

        return f"Weather in {name}, {country}:\nTemperature: {temp}°C\nFeels like: {feels_like}°C\nHumidity: {humidity}%\nWind speed: {wind_speed} km/h\nPrecipitation: {precip} mm"
    except Exception as e:
        return f"Error fetching weather data: {str(e)}"


# Fallback search tool
search = DuckDuckGoSearchRun()

tools = [get_weather, search]

# 3. Create Agent
system_message = (
    "You are a precise weather assistant. Use the get_weather tool to retrieve "
    "accurate, real-time weather data including exact temperature readings. "
    "Always report temperatures with one decimal place precision (e.g., 15.3°C). "
    "Only use the search tool if get_weather fails or for additional context. "
    "Provide temperature in Celsius by default, unless user specifies Fahrenheit."
)

agent_executor = create_agent(llm, tools, system_prompt=system_message)

# 5. Interactive Loop
print("=== Weather Search Agent ===")
print("Ask me about the weather in any location!")
print("Type 'quit' or 'exit' to stop.\n")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break

    if not user_input:
        continue

    try:
        response = agent_executor.invoke({"messages": [("user", user_input)]})
        print(f"\nAgent: {response['messages'][-1].content}\n")
    except Exception as e:
        print(f"Error: {e}\n")
