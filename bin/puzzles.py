import tkinter, os, assets

class WindowHandler(tkinter.Tk):
        
        def __init__(self, windowGeometry="0x0", windowTitle="None", iconifyWindow = False) -> None:
            super().__init__()
            self.geometry(windowGeometry)
            if iconifyWindow:
                self.iconify()
            self.title(windowTitle)
            self.mainloop()
            
class TextInput:
    
    def __init__(self, randomint) -> None:
        self.fileObj = open(assets.windowNames[randomint], 'w')
        self.fileObj.close()
        