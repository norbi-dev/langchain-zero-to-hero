from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. Initialize Gemma 3 (4B)
# temperature=0 ensures more consistent/factual responses
model = ChatOllama(model="gemma3:4b", temperature=0)

# 2. Setup Prompt with Memory Placeholder
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are Gemma 3, a highly capable local AI. You have a long context window and remember details from earlier in the chat.",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

# 3. Create the Chain
chain = prompt | model

# 4. Define Memory Storage
# This dictionary stores history objects by session_id
chat_storage = {}


def get_chat_history(session_id: str):
    if session_id not in chat_storage:
        chat_storage[session_id] = InMemoryChatMessageHistory()
    return chat_storage[session_id]


# 5. Wrap the Chain with History logic
chat_with_memory = RunnableWithMessageHistory(
    chain,
    get_chat_history,
    input_messages_key="input",
    history_messages_key="history",
)

# --- Usage ---

# Assign a specific ID for this conversation
config = {"configurable": {"session_id": "user_42_gemma"}}

# Round 1: Introduction
resp1 = chat_with_memory.invoke(
    {"input": "Hi! Remember this: my favorite color is 'Quantum Blue'."}, config=config
)
print(f"Gemma 3: {resp1.content}\n")

# Round 2: Memory Test
resp2 = chat_with_memory.invoke(
    {"input": "Do you remember my favorite color?"}, config=config
)
print(f"Gemma 3: {resp2.content}")
