from langgraph.graph import StateGraph, END
from agents.planner_node import plan_node
from agents.generation_node import generation_node
from agents.color_extractor_node import color_extractor
from agents.agent_state import AgentState

def build_graph(agent,plan_prompt, expert_prompt,color_exe_prompt):
    builder = StateGraph(AgentState)
    
    # Add nodes
    builder.add_node("planner", lambda state: plan_node(state, agent.model,plan_prompt))
    builder.add_node("generate", lambda state: generation_node(state, agent.model,expert_prompt))
    builder.add_node("extracter", lambda state: color_extractor(state, agent.model,color_exe_prompt))
    
    # Set entry point
    builder.set_entry_point("planner")
    
    # Add edges
    builder.add_edge("planner", "generate")
    
    builder.add_edge("generate","extracter")
    
    builder.add_edge("extracter",END)
    # Compile the graph
    return builder.compile()