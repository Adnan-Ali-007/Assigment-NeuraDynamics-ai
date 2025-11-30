import os
import requests


def llm_node(state):
    api_key = os.getenv("OPENROUTER_API_KEY")

    user_input = state.get("user_input", "")
    context = state.get("context", "")
    weather_info = state.get("weather_info", "")

    if weather_info and not context:
        return {"final_answer": weather_info}

    messages = []
    
    if context:
        system_prompt = (
            "You are a helpful assistant answering questions about a document.\n"
            "ONLY use the provided CONTEXT to answer. "
            "If the answer is not in the CONTEXT, respond with: 'This information is not available in the provided document.'"
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"CONTEXT:\n{context}\n\nQUESTION: {user_input}"}
        ]
    else:
        messages = [{"role": "user", "content": user_input}]

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "Weather PDF RAG Assistant"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "temperature": 0.0
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        json=payload,
        headers=headers,
        timeout=30
    )

    data = response.json()
    final_answer = data["choices"][0]["message"]["content"]

    return {"final_answer": final_answer}
