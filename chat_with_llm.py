"""First chat interaction with a loacl LLM using LangChain Ollama integration."""

from langchain_ollama import ChatOllama


def main():
    llm = ChatOllama(model="gemma3:4b", temperature=0.7)
    text = "Suggest a personalized workout routine for someone looking to improve cardiovascular endurance and prefers outdoor activities."
    response = llm.invoke(text)
    print("Response:", response.content)


if __name__ == "__main__":
    main()
