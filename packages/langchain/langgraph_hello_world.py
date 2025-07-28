from typing import List, Dict, Any, TypedDict
from langgraph.graph import StateGraph, START, END


# We now create an AgentState - shared data structure that keeps track of information as your application runs.
class AgentState(TypedDict):
    message: str


def greeting_node(state: AgentState) -> AgentState:
    """Simple node that adds a greeting message to the state"""
    
    state['message'] = "Hey " + state['message'] + ", how is your day going?"
    
    return state


def create_graph():
    """Create and compile the state graph"""
    # Initialize the graph
    graph = StateGraph(AgentState)
    
    # Add the greeting node
    graph.add_node("greeting", greeting_node)
    
    # Add edges
    graph.add_edge(START, "greeting")
    graph.add_edge("greeting", END)
    
    # Compile the graph
    app = graph.compile()
    
    return app


def main():
    # Create the graph
    app = create_graph()
    
    # Initial state
    initial_state = {
        "message": "Bob"
    }
    
    # Run the graph
    print("Running LangGraph Hello World...")
    print(f"Initial message: {initial_state['message']}")
    
    # Invoke the graph
    result = app.invoke(initial_state)
    
    print(f"Final message: {result['message']}")
    
    # Stream example
    print("\n--- Streaming Example ---")
    initial_state2 = {
        "message": "Alice"
    }
    
    for output in app.stream(initial_state2):
        for key, value in output.items():
            print(f"Node '{key}' output: {value}")


if __name__ == "__main__":
    main() 