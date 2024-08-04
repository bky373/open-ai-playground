import dotenv

dotenv.load_dotenv()

from langchain_upstage import ChatUpstage
from langchain_core.messages import HumanMessage, SystemMessage

chat = ChatUpstage(api_key="UPSTAGE_API_KEY")

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="Hi, how are you?")
]
response = chat.invoke(messages)
print(response)
