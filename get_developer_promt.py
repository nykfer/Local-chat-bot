def get_developer_prompt_for_note_taking_obsidian() -> str:
    promt = f"""
    You are a note-taking assistant that generates well-structured markdown notes for the Obsidian app.
    Your task is to create a markdown note based on the user’s provided context and preferences.
    """
    return promt.strip()

developer_promts = {
    "general_assistant": "",
    "note_taking_obsidian": get_developer_prompt_for_note_taking_obsidian(),
}