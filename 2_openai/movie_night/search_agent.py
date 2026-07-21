from agents import Agent, WebSearchTool, ModelSettings
from dotenv import load_dotenv
import os

load_dotenv(override=True)
MODEL_NAME = os.getenv("DEFAULT_MODEL_NAME", "gpt-5.4-mini")

INSTRUCTIONS = """
You are a movie-night research assistant. Given a search term, you search the web for that term
and produce a concise summary of relevant movie titles, brief descriptions, and where each is
currently streaming or available to watch. The summary must be 2-3 paragraphs and less than 300
words. Capture the main points and be succinct. Reply only with the summary.
"""

settings = ModelSettings(tool_choice="required")
tools = [WebSearchTool()]

search_agent = Agent(name="Movie Search Agent", instructions=INSTRUCTIONS, tools=tools, model=MODEL_NAME, model_settings=settings)
