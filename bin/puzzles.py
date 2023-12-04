import tkinter, os, assets, time
from tkinter import messagebox

class WindowHandler(tkinter.Tk):
        
        def __init__(self, windowGeometry="0x0", windowTitle="None", iconifyWindow = False, widgets:list = [None]) -> None:
            super().__init__()
            self.geometry(windowGeometry)
            if iconifyWindow:
                self.iconify()
            self.title(windowTitle)
            
            
            self.mainloop()

class Message(tkinter.Tk):
    
    def __init__(self, characters) -> None:
        super().__init__()
        
        self.geometry("0x0")
        self.iconify()
        self.title("")
        
        listname = []
        for i in characters:
            listname.append(i)
        listname = listname[::-1] #INVERT
        
        for element in listname:
            time.sleep(5)
            messagebox.showinfo(" ", element)
            
        self.quit()
        
    
class TextInput:
    
    def __init__(self, name, type = None) -> None:
        self.fileObj = open(name, 'w')
        match type:
            case 0:
                self.namePuzzle(name)
                
    def namePuzzle(self, name):
        
        self.fileObj.write("The answer to this puzzle requires an input of text into it when you think you have the answer type it into the terminal")
        self.fileObj.close()
        
        
        listname = []
        for i in name:
            listname.append(i)
        listname = listname[::-1] #INVERT
        
        nameinv = ''.join(listname)
        
        while True:
            self.fileObj = open(name, 'r')
            data = self.fileObj.read() #APPLY
            if data == nameinv:
                self.fileObj.close()
                break
            self.fileObj.close()
            time.sleep(1)
        
        os.remove(name)
            
        