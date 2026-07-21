from agents import Runner, trace, gen_trace_id
from search_agent import search_agent
from planner_agent import planner_agent, MovieSearchItem, MovieSearchPlan
from writer_agent import writer_agent, MoviePick
from clarifier_agent import clarifier_agent
import asyncio


class MovieNightManager:

    async def get_clarifying_questions(self, initial_input: str):
        """TODO(learning exercise): implement this to call the clarifier agent you build in
        clarifier_agent.py.

        Mirror plan_searches/write_pick below: one Runner.run(...) call, return result.final_output.

        Steps:
          1. Finish clarifier_agent.py (defines `ClarifyingQuestions` + `clarifier_agent`).
          2. Add `from clarifier_agent import clarifier_agent, ClarifyingQuestions` to this file's imports.
          3. result = await Runner.run(clarifier_agent, f"User's initial request: {initial_input}")
          4. return result.final_output   # a ClarifyingQuestions instance with a `.questions` list

        This is called from app.py's stage-1 handler (also a TODO — see app.py).
        """
        questions = await Runner.run(clarifier_agent, f"User's initial request: {initial_input}")
        return questions.final_output

    async def run(self, initial_input: str, qa_pairs: list[tuple[str, str]]):
        """Run the movie-picking process, yielding status updates and the final pick."""
        trace_id = gen_trace_id()
        with trace("Movie Night trace", trace_id=trace_id):
            yield f"Starting movie search. Trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            combined_query = self._build_combined_query(initial_input, qa_pairs)
            search_plan = await self.plan_searches(combined_query)
            yield f"Search plan ready, starting {len(search_plan.searches)} searches..."
            search_results = await self.perform_searches(search_plan)
            yield "Searches complete, picking tonight's movie..."
            pick = await self.write_pick(combined_query, search_results)
            yield "Pick ready!"
            yield pick.markdown_report

    def _build_combined_query(self, initial_input: str, qa_pairs: list[tuple[str, str]]) -> str:
        """Fold the initial free-text input and any non-empty question/answer pairs into one prompt string."""
        lines = [f"Initial request: {initial_input}"]
        for question, answer in qa_pairs:
            if answer and answer.strip():
                lines.append(f"Q: {question}\nA: {answer.strip()}")
        return "\n".join(lines)

    async def plan_searches(self, combined_query: str) -> MovieSearchPlan:
        """Plan the searches to perform for the combined query."""
        result = await Runner.run(planner_agent, f"Query: {combined_query}")
        return result.final_output

    async def perform_searches(self, search_plan: MovieSearchPlan) -> list[str]:
        """Perform the planned searches in parallel."""
        tasks = [self.search(item) for item in search_plan.searches]
        return await asyncio.gather(*tasks)

    async def search(self, item: MovieSearchItem) -> str | None:
        """Perform a single search."""
        input_message = f"Search term: {item.query}\nReason for searching: {item.reason}"
        result = await Runner.run(search_agent, input_message)
        return result.final_output

    async def write_pick(self, combined_query: str, search_results: list[str]) -> MoviePick:
        """Write the final movie pick."""
        input_message = f"Original request (with clarifying answers): {combined_query}\nSummarized search results: {search_results}"
        result = await Runner.run(writer_agent, input_message)
        return result.final_output
