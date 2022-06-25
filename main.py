import pytesseract
import googletrans
from PIL import Image

if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

    im = Image.open(r'C:\Users\Jabri\Downloads\image.png')
    text = pytesseract.image_to_string(im, lang='ara')
    print(text)

