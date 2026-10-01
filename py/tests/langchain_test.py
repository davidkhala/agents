import os
import unittest

from langchain_core.messages import AIMessage

from davidkhala.ai.agent.langgraph import Agent, OpenRouterModel

api_key = os.environ.get('API_KEY')


class GetStartedTestCase(unittest.TestCase):

    def test_invoke(self):
        """https://langchain-ai.github.io/langgraph/#get-started"""

        def get_weather(city: str) -> str:
            """Get weather for a given city."""
            return f"It's always sunny in {city}!"

        free_model = "x-ai/grok-4.3" # chosen by https://openrouter.ai/models?supported_parameters=tools
        model = OpenRouterModel(api_key).init_chat_model(free_model)
        agent = Agent(
            model,
            "You are a helpful assistant",
            get_weather
        )
        r = agent.call("what is the weather in Hongkong")

        print(r) # TODO no actual response found


class ModelTestCase(unittest.TestCase):
    def test_openrouter(self):
        model = OpenRouterModel(api_key).init_chat_model("qwen/qwen3.8-27b:free")
        r: AIMessage = model.invoke("what is the weather in sf")
        print(r.content)


if __name__ == '__main__':
    unittest.main()
