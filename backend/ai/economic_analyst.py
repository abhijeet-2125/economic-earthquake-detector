import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from backend.ai.tools import (get_latest_eei,get_latest_forecast,get_top_anomalies)

llm = ChatOllama(model="llama3",temperature=0)

def ask_analyst(question):
    eei = get_latest_eei.invoke({})
    forecast = get_latest_forecast.invoke({})
    anomalies = get_top_anomalies.invoke({})

    template = """
    You are a senior macroeconomic risk analyst.
    Current Market Data: {eei}
    Forecast: {forecast}
    Historical Anomalies: {anomalies}
    User Question: {question}
    Give a professional explanation.
    """

    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm
    response = chain.invoke({"eei": eei,"forecast": forecast,"anomalies": anomalies,"question": question})
    return response.content

if __name__ == "__main__":
    answer = ask_analyst("Compare today's conditions with major historical anomalies.")
    print("\n")
    print(answer)