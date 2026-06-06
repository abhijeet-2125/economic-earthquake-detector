from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

# Create LLM
llm = ChatOllama(model="llama3")

# Prompt Template
template = """
You are an economics professor.
Answer this question:
{question}
"""

prompt = PromptTemplate.from_template(template)

# Creating Chain
chain = prompt | llm

# Running the Chain
response = chain.invoke({ "question": "What causes inflation?"})
print(response.content)