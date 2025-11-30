import os
from unittest.mock import patch, Mock

from src.agents.llm_node import llm_node


def make_response(json_data):
    m = Mock()
    m.json = Mock(return_value=json_data)
    return m


@patch("requests.post")
def test_llm_node_with_context_calls_openrouter(mock_post, monkeypatch):
    # Mock OpenRouter response
    mock_post.return_value = make_response({"choices": [{"message": {"content": "Answer from LLM"}}]})

    state = {"user_input": "what is X?", "context": "Context text here", "weather_info": ""}
    res = llm_node(state)

    # Ensure we got final_answer from the mocked response
    assert isinstance(res, dict)
    assert res.get("final_answer") == "Answer from LLM"

    # Check payload used temperature 0.0 and system prompt included
    args, kwargs = mock_post.call_args
    payload = kwargs.get("json", {})
    assert payload["temperature"] == 0.0
    messages = payload.get("messages", [])
    assert any(m.get("role") == "system" for m in messages)


@patch("requests.post")
def test_llm_node_returns_weather_directly_without_call(mock_post):
    # When weather_info present and no context, should return it directly
    state = {"user_input": "what's the weather", "context": "", "weather_info": "Sunny, 10C"}
    res = llm_node(state)

    assert res == {"final_answer": "Sunny, 10C"}
    mock_post.assert_not_called()
