import logging
from google.adk.agents.llm_agent import Agent
from .prompt.prompt import VALIDATE_PROMPT  
from .tool.tool import analyze_engine_health

# --- 0. Configuração de Logs (Best Practices) ---
logging.basicConfig(
    filename='engine_agent.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- 1. Definição do Agente (Prompt Engineering Refinado) ---

root_agent = Agent(
    model='gemini-2.5-pro', 
    name='engine_support',
    description="Sistema crítico de suporte à decisão de manutenção aeronáutica.",
    instruction=VALIDATE_PROMPT,
    tools=[analyze_engine_health],
)