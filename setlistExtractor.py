try: from PIL import Image, ImageEnhance, ImageTk
except ImportError: import Image, ImageEnhance, ImageTk
import pytesseract
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import re

pytesseract.tesseract_cmd = r'/user/local/Cellar/tesseract/4.0.0/bin/tesseract'

def getDominantColorsFromImage(image):
    
    colorPalleteCount = 256
    image_redux = image.convert("P",palette=Image.ADAPTIVE, colors=colorPalleteCount)
    image_redux = image_redux.convert("RGB")
    colors = image_redux.getcolors()
    
    # Remove black and white colors
    def isNotWhite(colorTuple):
        whiteTol = 610
        colorCount = colorTuple[0]
        color = colorTuple[1]
        if sum(color) > whiteTol:
            return False
        else:
            return True
    def isNotBlack(colorTuple):
        blackTol = 200
        colorCount = colorTuple[0]
        color = colorTuple[1]
        if sum(color) < blackTol:
            return False
        else:
            return True
            
    def isNotGrey(colorTuple):
        # TODO: Tune Eps
        eps = 20
        color=colorTuple[1]
        avVal=sum(color)/float(len(color))
        for triplet in color:
            if triplet < avVal-eps  or triplet > avVal+eps:
                return True
        return False
        
    colors = list(filter(isNotWhite,colors))
    colors = list(filter(isNotBlack,colors))
    colors = list(filter(isNotGrey,colors))
    colors.sort(key=lambda x: x[0])
    colors = [color[1] for color in colors]
    # Find Most different top color
    
    topColor1 = colors.pop(0)
    avVal = sum(topColor1)/float(len(topColor1))
    topColor1Profile = [True if (trip - avVal)/avVal >= 0 else False for trip in topColor1]
    
    for topColor2 in colors:
        avVal = sum(topColor2)/float(len(topColor2))
        topColor2Profile = [True if (trip - avVal)/avVal >= 0 else False for trip in topColor2]
        if topColor2Profile == topColor1Profile:
            continue
        else:
            topColors = [topColor1, topColor2]
    return topColors

def promptUserForCorrections(initialText,image=None):
    ''' promptUserForCorrections is a GUI that allows the user to modify the text string
    
         Parameters:
            - initialText - initial string of text
    
         Return:
            - finalText - updated string of text submitted by the user
    
    '''
    # TODO: Better formatting of window, more descriptive labels, add some colors
    finalText = None
    

    colors = getDominantColorsFromImage(image)
    
    colorFG1 = colors[0]
    colorBG1 = colors[1]
    
    #TODO: Set colors to match poster
    def rgbfy(rgb):
        return "#%02x%02x%02x" % rgb
    master = tk.Tk()
    master.title("Setlist Editor")
    

    leftFrame = tk.Frame(master,width=300,height=400,bd=2,bg=rgbfy(colorBG1),\
     highlightbackground=rgbfy(colorFG1), highlightcolor=rgbfy(colorFG1), highlightthickness=3)
    rightFrame = tk.Frame(master,width=900,height=400,bd=2,bg=rgbfy(colorBG1),\
     highlightbackground=rgbfy(colorFG1), highlightcolor=rgbfy(colorFG1), highlightthickness=3)
    leftFrame.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)
    rightFrame.pack(side=tk.RIGHT,expand=True,fill=tk.BOTH)
    
    L1 = tk.Label(leftFrame, text='List of Artists',bg=rgbfy(colorBG1))        
    
    T1 = ScrolledText(leftFrame, width=40,borderwidth=2,bg=rgbfy(colorBG1))
    T1.insert(tk.INSERT,initialText)

    image_resized = image.resize((800,800), Image.ANTIALIAS)
    
    photo_img = ImageTk.PhotoImage(image_resized)
    L3 = tk.Label(rightFrame, image=photo_img,relief=tk.RAISED,bg=rgbfy(colorBG1))
    
    def callback():
        nonlocal finalText
        finalText = T1.get(1.0,tk.END)
        master.destroy()
        
    B1 = tk.Button(leftFrame, width=30, text = "Submit Setlist", bg=rgbfy(colorBG1),command=callback)

    L1.pack()
    T1.pack(expand=True,fill=tk.Y)
    L3.pack()
    B1.pack()
    T1.focus_set()
    
    tk.mainloop()
    
    return finalText
    
def convertImgToBlackOnWhite(image):
    '''Converts image to black-on-white (helps with OCR text recognition)'''

    # modify poster to make it readable (monochromatic)
    image_gray = image.convert('L')
        
    colors = image_gray.getcolors()
    
    # Calculate the white balance of the image (white pixels-black pixels)
    white_balance = sum([color[0] if color[1]>128 else -color[0] for color in colors])

    # If white balance is negative, invert the image to ensure black on white
    if white_balance > 0: 
        image_bw = image_gray.point(lambda x: 0 if x<128 else 255,'1')
    else: 
        image_bw = image_gray.point(lambda x: 255 if x<128 else 0,'1')
        
    return image_bw
    
def handleWeirdCharacters(text):
    # Weird Character Handling
    weird_characters = ['\n','-','»','«','>','°','*','~','.','=']
    text = text.replace('’','\'')
    for character in weird_characters:
        text = text.replace(character,'\n')
        
    #TODO: leading and trailing spaces
    text = re.sub(r'\s*\n\s*','\n',text)
    
    return text
    
def generateSetlistFromImage(image):
     
    # Open poster
    poster = Image.open(image)
        
    poster_bw = convertImgToBlackOnWhite(poster)

    #pull text from poster
    raw_poster_text = pytesseract.image_to_string(poster_bw)

    # format text by subbing out weird characters and spacing
    formatted_poster_text = handleWeirdCharacters(raw_poster_text)

    # Allow user to review and modify text
    poster_text = promptUserForCorrections(formatted_poster_text,poster)
    
    # Parse text based on new line
    setlist = re.split('\W*\n+\W*',poster_text)

    # Remove empty lines
    setlist = list(filter(None, setlist))
    
    return setlist

