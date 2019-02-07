'''

This function will be able to read a festival poster, generate a list of artists performing, look up their most popular tracks and create a playlist with them

'''
try: from PIL import Image, ImageEnhance
except ImportError: import Image, ImageEnhance
import pytesseract
import inspect

pytesseract.tesseract_cmd = r'/user/local/Cellar/tesseract/4.0.0/bin/tesseract'

# Open poster
poster = Image.open('crssd.jpg')

# modify poster to make it readable (monochromatic)
poster_gray = poster.convert('L')
poster_bw = poster_gray.point(lambda x: 0 if x<128 else 255,'1')
poster_bw.show()

#save off text from poster
poster_text = pytesseract.image_to_string(poster_bw)