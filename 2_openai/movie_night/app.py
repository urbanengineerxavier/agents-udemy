import gradio as gr
from dotenv import load_dotenv
from movie_manager import MovieNightManager

load_dotenv(override=True)


# ---------------------------------------------------------------------------
# Stage 2 (fully built): user answers -> full pipeline -> streamed markdown pick.
# ---------------------------------------------------------------------------
async def run_full_pipeline(initial_input: str, questions: list[str], a1: str, a2: str, a3: str):
    answers = [a1, a2, a3][: len(questions)]
    qa_pairs = list(zip(questions, answers))
    async for status_update in MovieNightManager().run(initial_input, qa_pairs):
        yield status_update


# ---------------------------------------------------------------------------
# Stage 1: free-text input -> 1-3 clarifying questions.
# ---------------------------------------------------------------------------
async def get_questions(initial_input: str):
    result = await MovieNightManager().get_clarifying_questions(initial_input)
    questions = result.questions

    updates = []
    for i in range(3):
        if i < len(questions):
            updates.append(gr.update(visible=True, label=questions[i], value=""))
        else:
            updates.append(gr.update(visible=False, value=""))
    updates.append(gr.update(visible=True))  # find_movie_button
    updates.append(initial_input)  # -> initial_input_state
    updates.append(questions)  # -> questions_state
    return updates
# ---------------------------------------------------------------------------


with gr.Blocks(title="Movie Night Picker") as ui:
    gr.Markdown("# 🎬 Movie Night Picker")

    initial_input_state = gr.State("")  # snapshot of the input that produced questions_state
    questions_state = gr.State([])  # the actual LLM-generated question text, needed in stage 2

    initial_textbox = gr.Textbox(
        placeholder="What are you in the mood for tonight?",
        label="Tell us about tonight",
        autofocus=True,
    )
    clarify_button = gr.Button("Get Clarifying Questions", variant="primary")

    answer_box_1 = gr.Textbox(visible=False)
    answer_box_2 = gr.Textbox(visible=False)
    answer_box_3 = gr.Textbox(visible=False)
    find_movie_button = gr.Button("Find My Movie", variant="primary", visible=False)

    report = gr.Markdown()

    clarify_outputs = [answer_box_1, answer_box_2, answer_box_3, find_movie_button,
                        initial_input_state, questions_state]
    clarify_button.click(get_questions, inputs=[initial_textbox], outputs=clarify_outputs)
    initial_textbox.submit(get_questions, inputs=[initial_textbox], outputs=clarify_outputs)

    find_movie_button.click(
        run_full_pipeline,
        inputs=[initial_input_state, questions_state, answer_box_1, answer_box_2, answer_box_3],
        outputs=report,
    )
    for box in (answer_box_1, answer_box_2, answer_box_3):
        box.submit(
            run_full_pipeline,
            inputs=[initial_input_state, questions_state, answer_box_1, answer_box_2, answer_box_3],
            outputs=report,
        )


if __name__ == "__main__":
    ui.launch(theme=gr.themes.Default(primary_hue="sky"))
