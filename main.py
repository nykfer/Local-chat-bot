import streamlit as st
from chat_gpt import ChatGPTService
from obsidian import add_note_to_obsidian
from get_developer_promt import developer_promts
import os

def initialize_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "show_save_form" not in st.session_state:
        st.session_state.show_save_form = False
    if "current_response" not in st.session_state:
        st.session_state.current_response = None
    if "selected_task" not in st.session_state:
        st.session_state.selected_task = None

def main():
    st.title("🤖 ChatGPT Assistant")
    
    # Initialize session state
    initialize_chat_history()
    
    # Sidebar for task selection and options
    with st.sidebar:
        st.header("Settings")
        
        # Task Selection
        st.subheader("Task Selection")
        task = st.selectbox(
            "What would you like to do?",
            [
                "Note Taking (Obsidian)",
                "General Assistant",
                # Add more tasks here as needed
            ],
            index=0
        )
        
        # Map friendly names to prompt keys
        task_to_prompt = {
            "Note Taking (Obsidian)": "note_taking_obsidian",
            "General Assistant": "general_assistant",
            # Add more mappings here as needed
        }
        
        # Update selected task in session state
        if st.session_state.selected_task != task_to_prompt[task]:
            st.session_state.selected_task = task_to_prompt[task]
            st.session_state.messages = []  # Clear chat history when task changes
        
        # Initialize ChatGPT service with selected prompt
        developer_prompt  = developer_promts[st.session_state.selected_task]
        chat_service = ChatGPTService(developer_prompt)
        
        # Chat Model Settings
        st.subheader("Model Settings")
        model = st.selectbox(
            "Select GPT Model",
            ["gpt-4.1", "gpt-4o", "gpt-3.5-turbo"],
            index=0
        )
        
        # File Upload Settings
        st.subheader("File Upload")
        uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx"])
        uploaded_images = st.file_uploader("Upload images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What's on your mind?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                if uploaded_file is not None:
                    temp_path = f"temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getvalue())
                    response = chat_service.generate_response_by_file_input(temp_path, prompt, model)
                    os.remove(temp_path)
                elif uploaded_images:
                    temp_paths = []
                    for img in uploaded_images:
                        temp_path = f"temp_{img.name}"
                        with open(temp_path, "wb") as f:
                            f.write(img.getvalue())
                        temp_paths.append(temp_path)
                    response = chat_service.generate_response_by_image_input(temp_paths, prompt, model)
                    for path in temp_paths:
                        os.remove(path)
                else:
                    response = chat_service.generate_response_by_text_input(prompt, model)

                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.current_response = response  # Save for later

    # Save Response Section (below chat)
    if st.session_state.current_response:
        st.divider()
        st.markdown("## 💾 Save Response")

        if st.button("Save to Obsidian", key="save_button"):
            st.session_state.show_save_form = True

        if st.session_state.show_save_form:
            with st.form(key="save_form"):
                col1, col2 = st.columns(2)
                with col1:
                    note_dir = st.selectbox(
                        "Select Directory",
                        ["Notion", "ChatGPT", "Projects", "Personal"],
                        index=0,
                        key="note_dir_select"
                    )
                with col2:
                    note_name = st.text_input(
                        "Note Name",
                        placeholder="Enter note name (without .md)",
                        key="note_name_input"
                    )

                submit_button = st.form_submit_button(label="Save Note")

                if submit_button:
                    if note_name:
                        try:
                            add_note_to_obsidian(note_name, st.session_state.current_response, note_dir)
                            st.success(f"✅ Saved to Obsidian in {note_dir}/{note_name}.md")
                            st.session_state.show_save_form = False
                        except Exception as e:
                            st.error(f"❌ Failed to save note: {str(e)}")
                    else:
                        st.error("Please enter a note name")

if __name__ == "__main__":
    main()