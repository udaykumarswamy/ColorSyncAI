from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai.chat_models import ChatOpenAI

from agents.agent_state import AgentState

def plan_node(state: AgentState, model: ChatOpenAI, plan_prompt):
    messages = [
        SystemMessage(content=plan_prompt),
        HumanMessage(content=state['task'])
    ]
    response = model.invoke(messages)
    return {"plan": response.content}