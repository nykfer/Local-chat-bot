# Import necessary libraries
from openai import OpenAI
import dotenv
import os
import base64

# Load environment variables from .env file
dotenv.load_dotenv()

class ChatGPTService:
    def __init__(self, developer_prompt: str = "You are a helpful assistant."):

        self.client = OpenAI(api_key=os.getenv("OPENAI-API-KEY"))

        self.developer_prompt = developer_prompt

    def generate_response_by_text_input(self, user_question: str, model:str = "gpt-4.1") -> str:
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": self.developer_prompt
                    },
                    {
                        "role": "user",
                        "content": f"{user_question}"
                    }
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error getting response: {str(e)}"
    
    def generate_response_by_file_input(self, file_path: str, user_question: str, model: str = "gpt-4.1") -> str:
        """Function for getting answer based on files input and user question."""
        
        try:
            with open(file_path, "rb") as f:
                uploaded_file = self.client.files.create(
                    file=f,
                    purpose="user_data"
                )
    
            response = self.client.responses.create(
                model=model,
                input=[
                    {
                        "role": "system",
                        "content": self.developer_prompt
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_file",
                                "file_id": uploaded_file.id,
                            },
                            {
                                "type": "input_text",
                                "text": user_question,
                            },
                        ]
                    }
                ]
            )
    
            return response.output_text
    
        except Exception as e:
            return f"Error processing file: {str(e)}"

      
    def generate_response_by_image_input(self, images_paths: list, user_question: str, model:str = "gpt-4.1") -> str:
        """Function for getting answer based on images input and user question."""
        
        # Function to encode the image
        def encode_image(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")

        try:
            # Create content list with the user question
            content = [{"type": "text", "text": user_question}]
            
            # Add all encoded images to content
            for path in images_paths:
                base64_image = encode_image(path)
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                })

            # Make the API call
            response = self.client.chat.completions.create(
                model=model,
                messages=[{
                        "role": "system",
                        "content": self.developer_prompt
                },
                {
                    "role": "user",
                    "content": content
                }]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error processing image: {str(e)}"
    
if __name__ == "__main__":
    
    file_path = "D:/універ книги/Операційне числення/Легеза_Олещенко Операційне числення.pdf"
    chat_gpt_service = ChatGPTService()
    question = "create a markdown note with detail explanation about Laplace transform"
    response = chat_gpt_service.generate_response_by_file_input(file_path, question)
    print(response)
    
    from obsidian import add_note_to_obsidian
    question = "Write a markdown note with the explanation of an integral. Add some formulas"
    response = chat_gpt_service.generate_response_by_text_input(question)
    print(response)
    add_note_to_obsidian("Integral_Explanation", response, "Notion")