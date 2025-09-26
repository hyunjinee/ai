from strands import Agent
from strands_tools import calculator, current_time

# Create an agent with tools
agent = Agent(tools=[calculator, current_time])

# Ask the agent a question that uses the available tools
message = """I am born in 1985, tell me my age in days."""

agent(message)
