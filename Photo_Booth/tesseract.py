from PIL import Image
import pytesseract


def transcript(file_input): 
    filename = "media/{}".format(file_input.name)
    pytesseract.pytesseract.tesseract_cmd ='C:/Program Files/Tesseract-OCR/tesseract.exe'  
    text = pytesseract.image_to_string(Image.open(filename))
    return text