try: from PIL import Image, ImageEnhance, ImageTk
except ImportError: import Image, ImageEnhance, ImageTk
import pytesseract
import tkinter as tk
from tkinter import filedialog as tkfd
from tkinter.scrolledtext import ScrolledText
import setlistExtractor

class playlistGenWindow:
        
    @staticmethod
    def rgbfy(rgb):
        return "#%02x%02x%02x" % rgb
    
    
    def UpdateColorTheme(self):
        colors = setlistExtractor.GetDominantColorsFromImage(self.rawImage)
        fgColor = playlistGenWindow.rgbfy(colors[0])
        bgColor = playlistGenWindow.rgbfy(colors[1])
        
        self.master.configure(background=bgColor)
        for element in self.elem.keys():
            self.elem[element].config(fg = fgColor,
                                 bg = bgColor,
                                 highlightbackground = bgColor)
    
    def ProcessAndUpdateImage(self):
        self.rawImage = Image.open(self.sourceLocation)
        image_resized = self.rawImage.resize((600,500), Image.ANTIALIAS)
        photo_img = ImageTk.PhotoImage(image_resized)
        self.elem['TargetImage'].configure(image = photo_img)
        self.elem['TargetImage'].image = photo_img
        self.UpdateColorTheme()
        
    def PullFromPoster(self):
        self.sourceLocation = tkfd.askopenfilename()
        setlist = setlistExtractor.generateSetlistFromImage(self.sourceLocation)
        # TODO: Clear old text
        self.elem['ListItems'].insert(tk.INSERT,'\n'.join(setlist))
        self.ProcessAndUpdateImage()
        
        
    def PullFrom1001Tracklists(self):
        print('Pull from 1001Tracklists Not Implemented Yet')
    
    def cbPullDataFromSource(self):
        # TODO: Use Dictionary as switch statement
        mode = self.sourceMode.get()
        if mode == "Poster Generator":
            self.PullFromPoster()
        elif mode == "1001Tracklist Generator":
            self.PullFrom1001Tracklists()
        else:
            print('Source Mode Not Implemented')
        
    def cbSubmit(self):
        rawText = self.ListItems.get(1.0,tk.END)
        setlist = rawText.split('\n')
        # Remove empty lines
        self.finalSetlist = list(filter(None, setlist))
        
        setlistExtractor.CreatePlaylist(self.finalSetlist ,
                                        self.elem['PlaylistName'].get())
        # TODO: Create a progress bar instead of destroying
        master.destroy()
    
        
    def __init__(self):
        defaultBgColor = 'DarkOrange4'
        defaultFgColor = 'white'
        
        self.finalSetlist = None
        self.sourceLocation = None
        self.elem = {}
        self.rawImage = None
        
        self.master = tk.Tk()
        self.master.title("Spotify Playlist Generator")
        self.master.configure(background=defaultBgColor)
        # Top Frame Items
        self.elem['PlaylistNameLabel'] = tk.Label(self.master, 
                                             text='Playlist Name:',
                                             width=20,
                                             fg=defaultFgColor,
                                             bg=defaultBgColor)
        self.elem['PlaylistName'] = tk.Entry(self.master,
                                        width=40,
                                        fg=defaultFgColor,
                                        bg=defaultBgColor)
        
        self.sourceMode = tk.StringVar(self.master) 
        self.sourceMode.set("Poster Generator")
        self.elem['ModeDropdown'] = tk.OptionMenu(self.master,
                                        self.sourceMode,
                                        "Poster Generator",
                                        "1001Tracklist Generator")
                                        
        self.elem['ModeDropdown'].config(width=20 , bg=defaultBgColor, fg=defaultFgColor)
        
        # Either a url or a file location
        self.elem['SourceLoc'] = tk.Button(self.master, 
                                        text='Select Data Source', 
                                        command=self.cbPullDataFromSource, 
                                        width=40,
                                        fg=defaultFgColor,
                                        highlightbackground=defaultBgColor)
        
        self.elem['ListTitle'] = tk.Label(self.master,
                                    text = 'List of Found Items:',
                                    width = 60, 
                                    fg=defaultFgColor,
                                    bg=defaultBgColor)
                                    
        self.elem['ListItems'] = ScrolledText(self.master, 
                                      width = 60,
                                      fg=defaultFgColor,
                                      bg=defaultBgColor,
                                      highlightbackground=defaultBgColor,
                                      borderwidth = 2,
                                      relief = tk.RAISED)
                                        
        # TODO: Add Logo As Default Image
        self.elem['TargetImage'] = tk.Label(self.master,
                                    fg=defaultFgColor,
                                    bg=defaultBgColor,
                                    relief = tk.RAISED)
                                    
        self.elem['SubmitButton'] = tk.Button(self.master,
                                      text = "Generate Playlist",
                                      command=self.cbSubmit,
                                      width = 40,
                                      fg=defaultFgColor,
                                      highlightbackground=defaultBgColor)


            
        # Packing
        self.elem['PlaylistNameLabel'].grid(row=0,column=0)
        self.elem['PlaylistName'].grid(row=0,column=1,columnspan=2)
        self.elem['ModeDropdown'].grid(row=0,column=3)
        self.elem['SourceLoc'].grid(row=0,column=4, columnspan=2)
        
        self.elem['ListTitle'].grid(row=1,column=0,columnspan=3)
        self.elem['ListItems'].grid(row=2,rowspan=8,column=0,columnspan=3)
        self.elem['TargetImage'].grid(row=1,rowspan=10,column=3,columnspan=3)
        self.elem['SubmitButton'].grid(row=11,column=0,columnspan=3)
        #self.ListItems.focus_set()
    
        tk.mainloop()
        


        
        
if __name__=="__main__":
    window = playlistGenWindow()
    