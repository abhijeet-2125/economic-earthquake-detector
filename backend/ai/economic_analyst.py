import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
from langchain_ollama import ChatOllama
from backend.ai.tools import (get_latest_eei,get_latest_forecast,get_top_anomalies)

llm = ChatOllama( model="llama3",temperature=0)
tools = [get_latest_eei,get_latest_forecast,get_top_anomalies]
print("Economic Analyst Initialized")
print("Tools Loaded:", len(tools))