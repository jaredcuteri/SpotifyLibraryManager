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
        defaultBgColor = 'DarkOrange4'
        defaultFgColor = 'white'
        
        self.finalText = None
        
        self.master = tk.Tk()
        self.master.title("Spotify Playlist Generator")
        self.master.configure(background=defaultBgColor)
        # Top Frame Items
        self.PlaylistNameLabel = tk.Label(self.master, 
                                             text='Playlist Name:',
                                             width=20,
                                             fg=defaultFgColor,
                                             bg=defaultBgColor)
        self.PlaylistName = tk.Entry(self.master,
                                        width=40,
                                        fg=defaultFgColor,
                                        bg=defaultBgColor)
        
        self.sourceMode = tk.StringVar(self.master) 
        self.sourceMode.set("Poster Generator")
        self.ModeDropdown = tk.OptionMenu(self.master,
                                        self.sourceMode,
                                        "Poster Generator",
                                        "1001Tracklist Generator")
                                        
        self.ModeDropdown.config(width=20 , bg=defaultBgColor, fg=defaultFgColor)
        
        # Either a url or a file location
        self.SourceLocation = tk.Button(self.master, 
                                        text='Select Data Source', 
                                        command=self.cbOpenPoster, 
                                        width=40,
                                        fg=defaultFgColor,
                                        highlightbackground=defaultBgColor)
        
        self.ListTitle = tk.Label(self.master,
                                    text = 'List of Found Items:',
                                    width = 60, 
                                    fg=defaultFgColor,
                                    bg=defaultBgColor)
                                    
        self.ListItems = ScrolledText(self.master, 
                                      width = 60,
                                      fg=defaultFgColor,
                                      bg=defaultBgColor,
                                      highlightbackground=defaultBgColor,
                                      borderwidth = 2)
                                        
        #self.T1.insert(tk.INSERT,initialText)
        # TODO: Add Logo As Default Image
        self.TargetImage = tk.Label(self.master,
                                    width = 60,
                                    fg=defaultFgColor,
                                    bg=defaultBgColor,
                                    relief = tk.RAISED)
                                    
        self.SubmitButton = tk.Button(self.master,
                                      text = "Generate Playlist",
                                      width = 40,
                                      fg=defaultFgColor,
                                      highlightbackground=defaultBgColor)


            
        # Packing
        self.PlaylistNameLabel.grid(row=0,column=0)
        self.PlaylistName.grid(row=0,column=1,columnspan=2)
        self.ModeDropdown.grid(row=0,column=3)
        self.SourceLocation.grid(row=0,column=4, columnspan=2)
        
        self.ListTitle.grid(row=1,column=0,columnspan=3)
        self.ListItems.grid(row=2,rowspan=8,column=0,columnspan=3)
        self.TargetImage.grid(row=1,rowspan=11,column=3,columnspan=3)
        self.SubmitButton.grid(row=11,column=0,columnspan=3)
        #self.ListItems.focus_set()
    
        tk.mainloop()
        

        
    @staticmethod
    def rgbfy(rgb):
        return "#%02x%02x%02x" % rgb
        
        
if __name__=="__main__":
    window = playlistGenWindow()
    