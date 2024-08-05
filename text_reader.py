from PIL import Image
import pytesseract
import os
import random
from pdf_to_img import pdf_to_pil_images

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def extract_text_from_image(img):
    text = pytesseract.image_to_string(img)
    text = text.replace("\n", " ")
    return text


def make_new_txt_file(pdf_path, lines):
    txt_path = pdf_path.replace(".pdf", ".txt")
    with open(txt_path, "w") as f:
        f.write(lines)


def pdf_to_text(pdf_path):
    images = pdf_to_pil_images(pdf_path)
    lines = ""
    lines += f"Converting this pdf to text: {pdf_path}\n"
    lines += f"There are {len(images)} pages in this pdf\n\n\n"
    for i, image in enumerate(images):
        lines += f"Page {i+1}\n"
        lines += extract_text_from_image(image) + "\n"
        lines += "\n\n"
    make_new_txt_file(pdf_path, lines)


def pdfs_to_text(pdf_folder_path):
    files = os.listdir(pdf_folder_path)
    for file in files:
        path = os.path.join(pdf_folder_path, file)
        pdf_to_text(path)


if __name__ == "__main__":
    pdfs_path = r"C:\Users\matt\Desktop\phil_readings"
    for file in os.listdir(pdfs_path):
        pdf_path = os.path.join(pdfs_path, file)
        pdf_to_text(pdf_path)
