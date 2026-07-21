from pydantic import BaseModel, Field
from agents import Agent
from dotenv import load_dotenv
import os

load_dotenv(override=True)
MODEL_NAME = os.getenv("DEFAULT_MODEL_NAME", "gpt-5.4-mini")

INSTRUCTIONS = """
You are a movie-night curator. You will be given the user's original request, folded together
with their answers to some clarifying questions, plus summarized web search results about what's
currently streaming. Pick exactly ONE best recommendation that matches the stated mood, genre,
audience, and streaming access.

Write `markdown_report` with:
- The movie title as a heading
- A "Why it fits" section that ties explicitly back to the clarifying answers
- A spoiler-free synopsis
- A "Where to watch" line naming the streaming service

Also list 1-2 runner-up alternatives in `runner_up_picks` in case the main pick isn't available.
"""


class MoviePick(BaseModel):
    short_summary: str = Field(description="A 1-2 sentence teaser of the recommended movie and why it fits.")
    markdown_report: str = Field(description="The final movie recommendation in markdown: title, why it fits, spoiler-free synopsis, and where to watch/stream.")
    runner_up_picks: list[str] = Field(description="1-2 alternate movie suggestions in case the main pick isn't available.")


writer_agent = Agent(name="Movie Writer Agent", instructions=INSTRUCTIONS, model=MODEL_NAME, output_type=MoviePick)
