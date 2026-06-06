import pandas as pd
import sys
from langchain.tools import tool
from langchain_ollama import ChatOllama
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from sqlalchemy import text
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from backend.database.database import engine

@tool
def get_latest_eei():
    """
    Returns the current Economic Earthquake Index,
    risk level, contagion score and flight-to-safety score.
    Use this tool whenever the user asks about
    current market conditions or risk.
    """
    query = """
    SELECT *
    FROM eei_daily
    ORDER BY date DESC
    LIMIT 1
    """

    df = pd.read_sql(text(query),engine)
    row = df.iloc[0]
    return (
        f"EEI: {row['economic_earthquake_index']}, "
        f"Risk: {row['risk_level']}, "
        f"CACI: {row['cross_asset_contagion_index']}, "
        f"FTSI: {row['flight_to_safety_index']}"
    )

@tool
def get_latest_forecast():
    """
    Returns the latest forecasted EEI value.
    """
    query = """
    SELECT *
    FROM eei_forecasts
    ORDER BY date DESC
    LIMIT 1
    """

    df = pd.read_sql(text(query), engine)
    row = df.iloc[0]
    return (
        f"Forecasted EEI: "
        f"{row['prediction']}"
    )

@tool
def get_top_anomalies():
    """
    Returns the most severe historical market crises
    detected by the system.
    Use this tool when comparing today's conditions
    with past crises or anomalies.
    """
    query = """
    SELECT
        date,
        economic_earthquake_index,
        risk_level
    FROM eei_anomalies
    WHERE anomaly = -1
    ORDER BY anomaly_score
    LIMIT 10
    """

    df = pd.read_sql(text(query),engine)
    return df.to_string(index=False)

llm = ChatOllama(model="llama3")
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm=llm,tools=[get_latest_eei, get_latest_forecast, get_top_anomalies], prompt=prompt)

agent_executor = AgentExecutor(agent=agent,tools=[get_latest_eei, get_latest_forecast, get_top_anomalies],verbose=True,max_iterations=5,handle_parsing_errors=True)
response = agent_executor.invoke({"input":"Compare today's conditions with major historical anomalies."})
print("\nFINAL ANSWER:")
print(response["output"])