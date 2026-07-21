from pydantic import BaseModel, Field
from agents import Agent
import os
from dotenv import load_dotenv
load_dotenv(override=True)

MODEL_NAME = os.getenv("DEFAULT_MODEL_NAME", "gpt-5.4-mini")

# TODO(learning exercise): build this agent yourself, mirroring planner_agent.py's shape
# (pydantic output model -> INSTRUCTIONS string -> Agent(... output_type=...)).
#
# 1. Define `ClarifyingQuestions(BaseModel)` with a `questions: list[str]` field (use `Field(description=...)`
#    like MovieSearchItem/MovieSearchPlan in planner_agent.py). This model becomes `output_type`, so the
#    Agents SDK forces the LLM's response into this exact shape.
#
# 2. Write `INSTRUCTIONS`: a movie-night assistant that reads the user's free-text request and asks what's
#    still ambiguous before a good recommendation can be made — e.g. genre/mood, who's watching (solo/date/
#    family/friends), which streaming services are available, tone/energy level, runtime constraints, new
#    release vs. classic. Tell it to skip anything the user already answered, order questions by importance,
#    and output between 1 and 3 short single-sentence questions — never more than 3.
#
# 3. Decide how you'll enforce "1 to 3 questions": prompt instructions alone (simplest, matches how
#    planner_agent.py's HOW_MANY_SEARCHES is instruction-driven, not schema-enforced), or add a pydantic
#    `field_validator` on `questions` as a defensive clamp. If you add a validator, make it CLAMP/truncate
#    rather than raise — Runner.run(..., output_type=...) has no retry loop, so a raised ValidationError
#    would crash stage 1 of the UI with no recovery path. A reasonable clamp: strip blanks, cap at 3, and
#    fall back to one generic question if the model returns zero.
#
# 4. Construct the agent:
#    clarifier_agent = Agent(name="Clarifier Agent", instructions=INSTRUCTIONS, model=MODEL_NAME, output_type=ClarifyingQuestions)
#
# Reference: 2_openai/deep_research/planner_agent.py for the exact structural pattern to mirror.

INSTRUCTIONS = """
You are a movie-night assistant that reads the user's free-text request and asks what's
still ambiguous before a good recommendation can be made — e.g. genre/mood, who's watching (solo/date/
family/friends), which languages are preferred, tone/energy level, runtime constraints, new
release vs. classic. Skip anything the user already answered, order questions by importance,
and output between 1 and 3 short single-sentence questions — never more than 3
"""

class ClarifyingQuestions(BaseModel):
    questions: list[str] = Field(description="A list of clarifying questions to ask the user about their movie-night request.")

clarifier_agent = Agent(name="Clarifier Agent",instructions=INSTRUCTIONS, model=MODEL_NAME, output_type=ClarifyingQuestions)
