from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

llm = ChatOllama(model="gemma3:4b", temperature=0.7)
prompt_template = PromptTemplate(
    template="What is a good name for a company that makes {product}?",
    input_variables=["product"],
)

chain = prompt_template | llm

# The model will 'parse' the city variable out of the input string
# and decide to call the tool.
response = chain.invoke(input={"product": "toys"})
print(f"Company name: {response.content}")
