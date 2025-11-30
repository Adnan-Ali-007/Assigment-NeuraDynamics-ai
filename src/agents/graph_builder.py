from langgraph.graph import StateGraph, END
import os
import requests
from typing import TypedDict, Any


class AgentState(TypedDict):
    user_input: str
    context: str
    weather_info: str
    route: str
    retriever: Any
    final_answer: str


def _keyword_fallback(query: str, texts: list, k: int = 3) -> list:
    query_words = set(w.lower() for w in query.split() if len(w) > 2)
    scored = []

    for text in texts:
        text_lower = text.lower()
        matches = sum(1 for word in query_words if word in text_lower)
        if matches > 0:
            scored.append((matches, text))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [text for _, text in scored[:k]]


def rag_node(state: AgentState) -> AgentState:
    user_input = state.get("user_input", "")
    retriever = state.get("retriever")

    if retriever is None:
        return {**state, "context": ""}

    context_docs = []

    try:
        context_docs = retriever.similarity_search(user_input, k=3)
    except Exception:
        context_docs = []

    if not context_docs or all(len(d.strip()) < 10 for d in context_docs):
        try:
            if hasattr(retriever, '_texts'):
                context_docs = _keyword_fallback(user_input, retriever._texts)
        except Exception:
            context_docs = []

    context = "\n---\n".join(context_docs) if context_docs else ""
    return {**state, "context": context}


def weather_node(state: AgentState) -> AgentState:
    from src.weather.weather_api import get_weather
    import re

    user_input = state.get("user_input", "")
    lower = user_input.lower()

    if "weather" not in lower and "temperature" not in lower:
        return {**state, "weather_info": ""}

    location = None

    m = re.search(r"weather\s+in\s+([A-Za-z][A-Za-z .,'-]+)", lower)
    if m:
        location = m.group(1).strip()

    if not location:
        m2 = re.match(r"([A-Za-z][A-Za-z .,'-]+)\s+weather", lower)
        if m2:
            location = m2.group(1).strip()

    if not location:
        m3 = re.search(r"weather\s+([A-Za-z][A-Za-z .,'-]+)", lower)
        if m3:
            location = m3.group(1).strip()

    if not location:
        location = "New York"

    weather_info = get_weather(location)
    return {**state, "weather_info": weather_info}


def router_node(state: AgentState) -> AgentState:
    user_input = state.get("user_input", "")

    if "weather" in user_input.lower() or "temperature" in user_input.lower():
        route = "weather"
    else:
        route = "rag"

    return {**state, "route": route}


def llm_node(state: AgentState) -> AgentState:
    try:
        from src.agents.llm_node import llm_node as external_llm
        res = external_llm(state)
        final = res.get("final_answer", "") if isinstance(res, dict) else ""
    except Exception as e:
        final = f"Error: {str(e)}"

    return {**state, "final_answer": final}


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", router_node)
    graph.add_node("rag", rag_node)
    graph.add_node("weather", weather_node)
    graph.add_node("llm", llm_node)

    graph.set_entry_point("router")

    graph.add_conditional_edges(
        "router",
        lambda x: x["route"],
        {
            "rag": "rag",
            "weather": "weather",
        },
    )

    graph.add_edge("rag", "llm")
    graph.add_edge("weather", "llm")
    graph.add_edge("llm", END)

    return graph.compile()
