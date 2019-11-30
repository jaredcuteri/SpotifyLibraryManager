try: from PIL import Image, ImageEnhance, ImageTk
except ImportError: import Image, ImageEnhance, ImageTk
import pytesseract
import tkinter as tk
from tkinter import filedialog as tkfd
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
import setlistExtractor

class playlistGenWindow:
    defBgColor = 'royalblue3'
    defFgColor = 'white'
    
    @staticmethod
    def rgbfy(rgb):
        return "#%02x%02x%02x" % rgb
    
    def UpdateColorTheme(self):
        colors = setlistExtractor.GetDominantColorsFromImage(self.rawImage)
        # TODO: Better color matching
        #fgColor = playlistGenWindow.rgbfy(colors[0])
        fgColor = 'White'
        bgColor = playlistGenWindow.rgbfy(colors[1])
        
        self.master.configure(background=bgColor)
        # Set the colors for all items that aren't text entry
        for masterElement in self.masterElem.keys():
            self.masterElem[masterElement].config(fg = fgColor,
                                 bg = bgColor,
                                 highlightbackground = bgColor)
                                 
    def ProcessAndUpdateImage(self):
        self.rawImage = Image.open(self.sourceLocation)
        image_resized = self.rawImage.resize((600,500), Image.ANTIALIAS)
        photo_img = ImageTk.PhotoImage(image_resized)
        self.masterElem['TargetImage'].configure(image = photo_img)
        self.masterElem['TargetImage'].image = photo_img
        self.UpdateColorTheme()
        
    def PullFromPoster(self):
        # TODO: Fix warning about multiple definitions of FIFinderSyncExtensionHost
        self.sourceLocation = tkfd.askopenfilename()
        setlist = setlistExtractor.generateSetlistFromImage(self.sourceLocation)
        # TODO: Clear old text
        self.masterElemEntry['ListItems'].insert(tk.INSERT,'\n'.join(setlist))
        self.ProcessAndUpdateImage()
        
    def PullFromURL(self):
        playlistURL = self.urlPromptElem['entry'].get()
        setlist, playlistName = setlistExtractor.GetTracksFromXML(playlistURL)
        self.masterElemEntry['ListItems'].insert(tk.INSERT,'\n'.join(setlist))
        self.masterElemEntry['PlaylistName'].insert(tk.INSERT,playlistName[0])
        self.urlPromptWindow.destroy()
    
    @staticmethod
    def PackWindow(elements):
        for _ , elem in elements.items():
            elem.pack()
            elem.configure(fg=playlistGenWindow.defFgColor,
                           bg=playlistGenWindow.defBgColor)
                           
    def PullFrom1001Tracklists(self):
        self.urlPromptWindow.deiconify()
        self.urlPromptWindow.lift()
        self.urlPromptWindow.attributes("-topmost", True)
    
    def cbPullDataFromSource(self):
        # TODO: Use Dictionary as switch statement
        mode = self.sourceMode.get()
        if mode == "Poster Generator":
            self.PullFromPoster()
        elif mode == "1001Tracklist Generator":
            self.PullFrom1001Tracklists()
        else:
            raise Exception('Source Mode Not Implemented')
        
    def cbSubmit(self):
        rawText = self.masterElemEntry['ListItems'].get(1.0,tk.END)
        setlist = rawText.split('\n')
        # Remove empty lines
        self.finalSetlist = list(filter(None, setlist))
        mode = self.sourceMode.get()
        if mode == "Poster Generator":
            setlistExtractor.PlaylistFromPoster(self.finalSetlist ,
                                        self.masterElemEntry['PlaylistName'].get())
        elif mode == "1001Tracklist Generator":
            setlistExtractor.PlaylistFrom1001Tracklist(self.finalSetlist)
        else:
            raise Exception('Source Mode Not Implemented')
        # TODO: Create a progress bar instead of destroying
        # TODO: Instead of destroying, reset gui
        self.master.destroy()
    
        
    def __init__(self):

        self.finalSetlist = None
        self.sourceLocation = None
        self.masterElem, self.masterElemEntry, self.masterElemAnim = {},{},{}
        self.rawImage = None
        
        self.master = tk.Tk()
        self.master.title("Spotify Playlist Generator")
        self.master.configure(background=playlistGenWindow.defBgColor)
        # Top Frame Items
        self.masterElem['PlaylistNameLabel'] = tk.Label(self.master, 
                                             text='Playlist Name:',
                                             width=20,
                                             fg=playlistGenWindow.defFgColor,
                                             bg=playlistGenWindow.defBgColor)
        self.masterElemEntry['PlaylistName'] = tk.Entry(self.master,
                                        width=40,
                                        fg='black',
                                        bg='white',
                                        relief = tk.RAISED)
        
        self.sourceMode = tk.StringVar(self.master) 
        self.sourceMode.set("Poster Generator")
        self.masterElem['ModeDropdown'] = tk.OptionMenu(self.master,
                                        self.sourceMode,
                                        "Poster Generator",
                                        "1001Tracklist Generator")
        self.masterElem['ModeDropdown'].config(width=20 , 
                                         bg=playlistGenWindow.defBgColor, 
                                         fg=playlistGenWindow.defFgColor
                                         )
        
        # Either a url or a file location
        self.masterElem['SourceLoc'] = tk.Button(self.master, 
                                        text='Select Data Source', 
                                        command=self.cbPullDataFromSource, 
                                        width=40,
                                        fg=playlistGenWindow.defFgColor,
                                        highlightbackground=playlistGenWindow.defBgColor)
        
        self.masterElem['ListTitle'] = tk.Label(self.master,
                                    text = 'List of Found Items:',
                                    width = 60, 
                                    fg=playlistGenWindow.defFgColor,
                                    bg=playlistGenWindow.defBgColor)
                                    
        self.masterElemEntry['ListItems'] = ScrolledText(self.master, 
                                      width = 60,
                                      fg='black',
                                      bg='white',
                                      highlightbackground='white',
                                      borderwidth = 2,
                                      relief = tk.RAISED)
                                        
        # TODO: Add Logo As Default Image
        self.masterElem['TargetImage'] = tk.Label(self.master,
                                    fg=playlistGenWindow.defFgColor,
                                    bg=playlistGenWindow.defBgColor)
                                    
        self.masterElem['SubmitButton'] = tk.Button(self.master,
                                      text = "Generate Playlist",
                                      command=self.cbSubmit,
                                      width = 40,
                                      fg=playlistGenWindow.defFgColor,
                                      highlightbackground=playlistGenWindow.defBgColor)

        s = ttk.Style()
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar", foreground='green', background='grey')
        self.masterElemAnim['ProgressBar'] = ttk.Progressbar(self.master,
                                                      style="green.Horizontal.TProgressbar",
                                                      orient=tk.HORIZONTAL,
                                                      length=800,
                                                      mode='determinate')
            
        # Packing
        self.masterElem['PlaylistNameLabel'].grid(row=0,column=0)
        self.masterElemEntry['PlaylistName'].grid(row=0,column=1,columnspan=2)
        self.masterElem['ModeDropdown'].grid(row=0,column=3)
        self.masterElem['SourceLoc'].grid(row=0,column=4, columnspan=2)
        
        self.masterElem['ListTitle'].grid(row=1,column=0,columnspan=3)
        self.masterElemEntry['ListItems'].grid(row=2,rowspan=8,column=0,columnspan=3)
        self.masterElem['TargetImage'].grid(row=1,rowspan=10,column=3,columnspan=3)
        self.masterElem['SubmitButton'].grid(row=11,column=0,columnspan=3)
        self.masterElemAnim['ProgressBar'].grid(row=12,column=0,columnspan=6)
        #self.ListItems.focus_set()
    
    
        self.urlPromptWindow = tk.Tk()
        self.urlPromptWindow.title("1001 Tracklists URL Input")
        self.urlPromptWindow.configure(background=playlistGenWindow.defBgColor)
        self.urlPromptElem = {}
        
        self.urlPromptElem['entry'] = tk.Entry(self.urlPromptWindow,width=150)
        self.urlPromptElem['entry'].insert(tk.END,'https://www.1001tracklists.com/tracklist/')
        self.urlPromptElem['button'] = tk.Button(self.urlPromptWindow, 
                                   text = "Pull Setlist", 
                                   width = 10,
                                   command = self.PullFromURL,
                                   fg=playlistGenWindow.defFgColor,
                                   highlightbackground=playlistGenWindow.defBgColor)
        playlistGenWindow.PackWindow(self.urlPromptElem)
        # Hide URL Prompt window until needed
        self.urlPromptWindow.withdraw()
        
        tk.mainloop()
        


        
        
if __name__=="__main__":
    window = playlistGenWindow()
    