from typing import List, Dict
from langgraph.graph import StateGraph, START, END
from langchain_ollama import OllamaLLM

# Defining State 
class State(Dict):
    messages: List[Dict[str, str]] 

# Initializing StateGraph
graph_builder = StateGraph(State)

# Initializing LLM
llm = OllamaLLM(model="llama3:latest")

# Defining chatbot function
def chatbot(state: State):
    response = llm.invoke(state["messages"])
    state["messages"].append({"role": "assistant", "content": response})  # Treat response as a string
    return {"messages": state["messages"]}

# Add nodes and edges (conversation where it will start and end)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Compiling the graph
graph = graph_builder.compile()

# Defining function to run chatbot
def stream_graph_updates(user_input: str):    
    state = {"messages": [{"role": "user", "content": user_input}]}
    for event in graph.stream(state):
        for value in event.values():
            print("Assistant:", value["messages"][-1]["content"])

# Run chatbot in a loop
if __name__ == "__main__":
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            stream_graph_updates(user_input)
        except Exception as e:
            print(f"An error occurred: {e}")
            break


