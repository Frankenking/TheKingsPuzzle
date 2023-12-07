import tkinter, os, time
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
            time.sleep(60)
            messagebox.showinfo(" ", element)
            
        self.quit()
        
    
class TextInput:
    
    def __init__(self, name, type = None, *args) -> None:
        match type:
            case 0:
                self.reversePuzzle(name)
            case 1:
                self.cypherPuzzle(name, args[0])
                
    def cypherPuzzle(self, name, key):
        
        encrypted = ""
        for i in range(len(name)):
            char = name[i]
            
            # Encrypt lowercase characters

            encrypted += chr((ord(char) + key - 97) % 26 + 97)
        
        while True:
            print(f"You are given a set of characters, '{''.join(encrypted)}', and then a number {key}")
            if input("Answer: ") == name:
                break
            else:
                os.system("cls")
                print("Wrong")
            
    
    def reversePuzzle(self, name):
        
        self.fileObj = open(name, 'w')
        self.fileObj.write("The answer to this puzzle requires an input of text into the terminal relating to the file, when you think you have the answer type it into the terminal")
        self.fileObj.close()
        
        listname = []
        for i in name:
            listname.append(i)
        listname = listname[::-1] #INVERT
        invname = ''.join(listname)
        
        while True:
            userInp = input("Answer: ")
            if userInp == invname:
                break
            else:
                os.system("cls")
                print("Wrong")
        
        os.remove(name)
            
        