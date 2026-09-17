from src.config import LLM_MODEL, LLM_TEMPERATURE, MAX_ITERATIONS, MEMORY_WINDOW
from src.routing import classify_intent, route_after_data_analyst, route_after_router


def test_model_name():
    assert LLM_MODEL == "openai/gpt-oss-120b"


def test_temp_low():
    assert 0 <= LLM_TEMPERATURE <= 0.5


def test_positive_caps():
    assert MAX_ITERATIONS > 0
    assert MEMORY_WINDOW > 0


def test_classify():
    assert classify_intent("data") == "data"
    assert classify_intent("viz please") == "viz"
    assert classify_intent("nope") == "data"


def test_router_edges():
    assert route_after_router({"intent": "data"}) == "data_analyst"
    assert route_after_router({"intent": "viz"}) == "viz_agent"
    assert route_after_router({"intent": "both"}) == "data_analyst"
    assert route_after_router({"intent": "general"}) == "report_writer"


def test_after_analyst():
    assert route_after_data_analyst({"intent": "both"}) == "viz_agent"
    assert route_after_data_analyst({"intent": "data"}) == "report_writer"
