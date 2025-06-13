import os

DIR_PATH = "D:\\obsidian"  # Use double backslashes for Windows paths

def add_note_to_obsidian(note_name: str, content: str, note_dir:str = "Notion") -> None:
    """Function to add a note to Obsidian vault."""
    if not note_name:
        raise ValueError("Note name cannot be empty")
    
    note_name = note_name.strip() + ".md"
    
    try:
        # Ensure the base directory exists
        if not os.path.exists(DIR_PATH):
            raise FileNotFoundError(f"Obsidian vault directory not found at {DIR_PATH}")
        
        # Create the subdirectory if it doesn't exist
        full_dir_path = os.path.join(DIR_PATH, note_dir)
        os.makedirs(full_dir_path, exist_ok=True)
        
        # Full path for the note file
        file_path = os.path.join(full_dir_path, note_name)
        
        # Create the note file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
                
    except Exception as e:
        raise Exception(f"Failed to create note: {str(e)}. Path attempted: {DIR_PATH}")