try: from PIL import Image, ImageEnhance, ImageTk
except ImportError: import Image, ImageEnhance, ImageTk
import pytesseract
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText
import re

class playlistGenWindow:
    
    def cbPosterMode(self):
        print('Poster Mode Selected')

    def cbTracklistMode(self):
        print('Tracklist Mode Selected')
    
    def cbOpenPoster(self):
        return askopenfilename(mode='r', **self.file_opt)
        
    def cbSubmit(self):
        self.finalText = self.T1.get(1.0,tk.END)
        master.destroy()
    
    
    def __init__(self):
        
        self.finalText = None
        
        self.master = tk.Tk()
        self.master.title("Spotify Playlist Generator")
        self.topFrame = tk.Frame(self.master,width=1200,height=100)
        self.leftFrame = tk.Frame(self.master,width=300,height=400,bd=2, highlightthickness=3)
        self.rightFrame = tk.Frame(self.master,width=900,height=400,bd=2, highlightthickness=3)
        
        self.topFrame.pack(expand=True,fill=tk.BOTH)
        self.leftFrame.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)
        self.rightFrame.pack(side=tk.RIGHT,expand=True,fill=tk.BOTH)
        
        # Top Frame Items
        self.PlaylistName = tk.Entry(self.master,width=300)
        
        self.currSourceMode = tk.StringVar(self.master) 
        self.currSourceMode.set("Poster Generator")
        self.SourceMode = tk.OptionMenu(self.master,self.currSourceMode,"Poster Generator","1001Tracklist Generator")
        # Either a url or a file location
        self.SourceLocation = tk.Button(self.master,text='Browse',command=self.cbOpenPoster)
        self.PullButton = tk.Button(self.topFrame,width=30,text="Pull From Source")
        
        # Left Frame Items
        self.TitleList = tk.Label(self.leftFrame, text='List of Items')        
        self.ItemsList = ScrolledText(self.leftFrame, width=40,borderwidth=2)
        #self.T1.insert(tk.INSERT,initialText)
        self.SubmitButton = tk.Button(self.leftFrame, width=30, text = "Generate Playlist")
        
        # Right Frame Items
        self.TargetImage = tk.Label(self.rightFrame,relief=tk.RAISED)
            
        # Packing
        self.PlaylistName.pack()
        self.SourceMode.pack()
        self.SourceLocation.pack()
        self.PullButton.pack()
        self.TitleList.pack()
        self.ItemsList.pack(expand=True,fill=tk.Y)
        self.TargetImage.pack()
        self.SubmitButton.pack()
        self.ItemsList.focus_set()
    
        tk.mainloop()
        

        
    @staticmethod
    def rgbfy(rgb):
        return "#%02x%02x%02x" % rgb
        
        
if __name__=="__main__":
    window = playlistGenWindow()
    