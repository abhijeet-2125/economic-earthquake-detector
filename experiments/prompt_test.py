from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

llm = ChatOllama(model="llama3")

template = """You are a financial analyst. Answer the following question: {question} """

prompt = PromptTemplate.from_template(template)

final_prompt = prompt.invoke(
    {
        "question":
        "What is inflation?"
    })

response = llm.invoke(final_prompt)
print(response.content)