from PyPDF2 import PdfReader, PdfWriter
import os

def split_pdf(input_path: str, start: int, finish: int, output_path: str = "D://output.pdf") -> None:
    """
    Split a PDF file and save selected pages to a new file.
    
    Args:
        input_path (str): Path to the input PDF file
        start (int): Start page index (0-based)
        finish (int): End page index (0-based)
        output_path (str): Path where to save the output PDF file
    """
    if not os.path.exists(input_path):
        raise ValueError("Input PDF file doesn't exist!")
    
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    # Validate page range
    total_pages = len(reader.pages)
    if start < 0 or finish > total_pages:
        raise ValueError(f"Invalid page range. PDF has {total_pages} pages.")
    
    # Add selected pages to the writer
    for index in range(start, min(finish, total_pages)):
        writer.add_page(reader.pages[index])
    
    # Save the output file
    with open(output_path, "wb") as output_file:
        writer.write(output_file)

    

if __name__ == "__main__":    
    # 1. Open the original PDF file
    reader = PdfReader("D://універ книги//English//Infotech Student's.pdf")  # Replace with your filename

    # 2. Create a new writer to save selected pages
    writer = PdfWriter()

    # 3. Define the page range (note: page numbers start at 0)
    start = 9   # 10th page (index 9)
    end = 13    # Up to (but not including) page 51

    # 4. Add the selected pages to the writer
    for i in range(start, min(end, len(reader.pages))):
        writer.add_page(reader.pages[i])

    # 5. Save to a new PDF file
    with open("D://універ книги//English//output_10_to_13.pdf", "wb") as output_file:
        writer.write(output_file)

    print("PDF pages 10–13 extracted successfully!")
