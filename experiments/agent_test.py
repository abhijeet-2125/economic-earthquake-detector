from langchain.tools import tool
from langchain_ollama import ChatOllama
from langchain.agents import (AgentExecutor,create_react_agent)
from langchain import hub

@tool
def square_number(number: str) -> int:
    """
    Returns square of a number.
    """
    number = int(number)
    return number * number

#calling llm object
llm = ChatOllama(model="llama3")
prompt = hub.pull("hwchase17/react")

#created agent
agent = create_react_agent(llm=llm,tools=[square_number],prompt=prompt)
agent_executor = AgentExecutor(agent=agent,tools=[square_number],verbose=True)

#question to ask on
response = agent_executor.invoke({ "input": "What is the square of 12?"})
print("\nFINAL ANSWER:")
print(response["output"])