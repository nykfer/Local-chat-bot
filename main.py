import streamlit as st
from chat_gpt import ChatGPTService
import os

def initialize_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def main():
    st.title("🤖 ChatGPT Assistant")
    
    # Initialize chat history
    initialize_chat_history()
    
    # Initialize ChatGPT service
    chat_service = ChatGPTService()
    
    # Sidebar for file uploads and options
    with st.sidebar:
        st.header("Settings")
        model = st.selectbox(
            "Select GPT Model",
            ["gpt-4.1", "gpt-4o"],
            index=0
        )
        
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

        # Generate response based on input type
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                if uploaded_file is not None:
                    # Save uploaded file temporarily
                    temp_path = f"temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getvalue())
                    response = chat_service.generate_response_by_file_input(temp_path, prompt, model)
                    os.remove(temp_path)
                elif uploaded_images:
                    # Save uploaded images temporarily
                    temp_paths = []
                    for img in uploaded_images:
                        temp_path = f"temp_{img.name}"
                        with open(temp_path, "wb") as f:
                            f.write(img.getvalue())
                        temp_paths.append(temp_path)
                    response = chat_service.generate_response_by_image_input(temp_paths, prompt, model)
                    # Clean up temporary files
                    for path in temp_paths:
                        os.remove(path)
                else:
                    response = chat_service.generate_response_by_text_input(prompt, model)
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()