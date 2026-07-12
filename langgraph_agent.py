from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from typing import TypedDict
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# State
class AgentState(TypedDict):
    question: str
    category: str
    answer: str

# Node 1 — التصنيف
def classify(state: AgentState):
    response = llm.invoke([
        SystemMessage(content="""Classify the question into ONE of:
        - greeting
        - technical
        - general
        Reply with ONLY the category name."""),
        HumanMessage(content=state["question"])
    ])
    category = response.content.strip().lower()
    print(f"📌 Category: {category}")
    return {"category": category}

# Node 2 — للتحية
def handle_greeting(state: AgentState):
    response = llm.invoke([
        SystemMessage(content="You are a warm and friendly assistant."),
        HumanMessage(content=state["question"])
    ])
    return {"answer": response.content}

# Node 3 — للتقني
def handle_technical(state: AgentState):
    response = llm.invoke([
        SystemMessage(content="You are a senior software engineer. Give detailed technical answers with examples."),
        HumanMessage(content=state["question"])
    ])
    return {"answer": response.content}

# Node 4 — للعام
def handle_general(state: AgentState):
    response = llm.invoke([
        SystemMessage(content="You are a knowledgeable assistant. Give clear and concise answers."),
        HumanMessage(content=state["question"])
    ])
    return {"answer": response.content}

# Conditional Edge — بيقرر يروح فين
def route(state: AgentState):
    category = state["category"]
    if category == "greeting":
        return "greeting"
    elif category == "technical":
        return "technical"
    else:
        return "general"

# بناء الـ Graph
graph = StateGraph(AgentState)

graph.add_node("classify", classify)
graph.add_node("greeting", handle_greeting)
graph.add_node("technical", handle_technical)
graph.add_node("general", handle_general)

graph.set_entry_point("classify")

# Conditional Edges
graph.add_conditional_edges(
    "classify",
    route,
    {
        "greeting": "greeting",
        "technical": "technical",
        "general": "general"
    }
)

graph.add_edge("greeting", END)
graph.add_edge("technical", END)
graph.add_edge("general", END)

app = graph.compile()

# تجربة
questions = [
    "مرحبا كيف حالك؟",
    "إيه الفرق بين RAG وFine-tuning؟",
    "كام عدد سكان مصر؟"
]

for q in questions:
    print(f"\n❓ السؤال: {q}")
    result = app.invoke({
        "question": q,
        "category": "",
        "answer": ""
    })
    answer_preview = result['answer'][:150]
    print(f"💬 الجواب: {answer_preview}...")
    print("-" * 50)