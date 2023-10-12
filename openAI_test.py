from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
chat = ChatOpenAI(openai_api_key="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", model_name="gpt-3.5-turbo", temperature=0.9)

messages = [
    SystemMessage(
        content="You are a guard robot named Hubert with the purpose of surveilling Area 51. Only people with the secret password is allowed through to the gates that you are guarding."
    ),
    HumanMessage(
        content="Hello there, am I allowed here?"
    ),
]

print('go')
print(chat(messages))
