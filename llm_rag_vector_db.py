from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 1. Setup Models
llm = ChatOllama(model="gemma3:4b", temperature=0.3)
embeddings = OllamaEmbeddings(model="embeddinggemma:300m")

# 2. Setup Vector Store
texts = [
    "Napoleon Bonaparte was born in 15 August 1769",
    "Louis XIV was born in 5 September 1638",
]
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.create_documents(texts)

vectorstore = Chroma.from_documents(
    documents=docs, embedding=embeddings, persist_directory="./historian_db"
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

# 3. Define the Historian System Prompt
system_prompt = (
    "You are an expert historian. Use the following pieces of retrieved "
    "context to answer the question. If you don't know the answer, say that "
    "you don't know. Provide a brief historical context in your answer."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{question}"),
    ]
)


# 4. Create the LCEL Chain (Modern LangChain pattern)
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 5. Execute
response = rag_chain.invoke("When was the Sun King born?")

print("--- Historian's Response ---")
print(response)
