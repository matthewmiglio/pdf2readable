import fitz  # PyMuPDF
from PIL import Image
import io


def pdf_to_pil_images(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    images = []

    # Iterate over each page
    for page_number in range(len(pdf_document)):
        # Get the page
        page = pdf_document.load_page(page_number)
        # Render page to an image (pixmap)
        pix = page.get_pixmap()
        # Convert pixmap to PIL Image
        img = Image.open(io.BytesIO(pix.tobytes()))
        images.append(img)

    return images
