from langchain_ollama import ChatOllama
llm = ChatOllama(model="llama3")
response = llm.invoke("Explain inflation in 3 lines.")
print(response.content)