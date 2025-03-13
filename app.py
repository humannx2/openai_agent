from dotenv import load_dotenv
import os
from agents import Agent, Runner

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

agent = Agent(name="Assistant", instructions="You are a helpful assistant",model="gpt-4o")

result = Runner.run_sync(agent, "Write a poem about a cat in the style of Edgar Allan Poe.")
print(result.final_output)

