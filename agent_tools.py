from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_react_agent
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Tool 1 — الحاسبة
@tool
def calculator(expression: str) -> str:
    """Calculate a math expression. Input should be a valid math expression like '2+2' or '10*5'."""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except:
        return "Error: Invalid expression"

# Tool 2 — الطقس
@tool
def get_weather(city: str) -> str:
    """Get the weather for a city."""
    weather_data = {
        "cairo": "☀️ Sunny, 35°C",
        "london": "🌧️ Rainy, 15°C",
        "new york": "⛅ Cloudy, 22°C",
        "aswan": "☀️ Very Hot, 42°C"
    }
    city_lower = city.lower()
    return weather_data.get(city_lower, f"Weather data not available for {city}")

# Tool 3 — البحث في المنتجات
@tool
def search_products(query: str) -> str:
    """Search for fashion products by name or category."""
    products = [
        {"name": "Classic White T-Shirt", "price": 29.99, "category": "T-Shirts"},
        {"name": "Slim Fit Jeans", "price": 79.99, "category": "Pants"},
        {"name": "Floral Summer Dress", "price": 59.99, "category": "Dresses"},
        {"name": "Running Sneakers", "price": 89.99, "category": "Shoes"},
    ]
    query_lower = query.lower()
    results = [p for p in products if query_lower in p["name"].lower() 
               or query_lower in p["category"].lower()]
    if results:
        return str(results)
    return "No products found"

# Agent مع الأدوات
tools = [calculator, get_weather, search_products]
agent = create_react_agent(llm, tools)

# تجربة
questions = [
    "What is 150 * 3 + 50?",
    "What's the weather in Aswan?",
    "Do you have any dresses?"
]

for q in questions:
    print(f"\n❓ {q}")
    result = agent.invoke({"messages": [("human", q)]})
    print(f"💬 {result['messages'][-1].content}")
    print("-" * 40)