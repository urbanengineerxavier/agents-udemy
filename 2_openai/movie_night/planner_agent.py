from pydantic import BaseModel, Field
from agents import Agent
import os
from dotenv import load_dotenv
load_dotenv(override=True)

MODEL_NAME = os.getenv("DEFAULT_MODEL_NAME", "gpt-5.4-mini")
HOW_MANY_MOVIE_SEARCHES = int(os.getenv("HOW_MANY_MOVIE_SEARCHES", 4))


INSTRUCTIONS = f"""
You are a movie-recommendation research assistant. Given a user's request for tonight's movie
(including any clarifying answers about genre/mood, who's watching, streaming services available,
tone/energy, runtime, or new-vs-classic), come up with a set of web searches to find currently
available movie options that match. Good search terms look like "best [mood] movies streaming now
on [service]" or "new [genre] releases [month] [year]". Output {HOW_MANY_MOVIE_SEARCHES} terms to
query for. For each search, explain in `reason` which part of the user's request it targets.
"""

class MovieSearchItem(BaseModel):
    reason: str = Field(description="Why this search will help find a good movie match.")
    query: str = Field(description="The search term to use for the web search.")


class MovieSearchPlan(BaseModel):
    searches: list[MovieSearchItem] = Field(description="A list of web searches to perform to find the best movie match.")

planner_agent = Agent(name="Movie Planner Agent", instructions=INSTRUCTIONS, model=MODEL_NAME, output_type=MovieSearchPlan)
