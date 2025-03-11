from langchain_openai.chat_models import ChatOpenAI

class Agent:
    def __init__(self, openai_api_key):
        self.model = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=openai_api_key,
            streaming=True,
        )