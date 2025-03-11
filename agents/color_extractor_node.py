from langchain_core.messages import SystemMessage, HumanMessage
from agents.agent_state import AgentState  

def color_extractor(state: AgentState,model,colo_exe_prompt):
    content = "\n\n".join(state['content'] or [])
    user_message = HumanMessage(
        content=f"{state['task']}\n\nHere is my plan:\n\n{state['plan']}")  
    messages = [
        SystemMessage(
            content=colo_exe_prompt.format(content=content)
        ),
        user_message
        ]
    response = model.invoke(messages)
    return {
        "draft": response.content,
    }