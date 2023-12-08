import tkinter, os, time
from tkinter import messagebox

#death to the threads

class passwordWindow(tkinter.Tk):
        
        def __init__(self, windowGeometry="0x0", windowTitle="None", iconifyWindow = False, widgets:list = [None]) -> None:
            super().__init__()
            self.passed = False
            self.titleName = windowTitle
            self.geometry(windowGeometry)
            if iconifyWindow:
                self.iconify()
            self.title(windowTitle)
            
            self.textAnswer = tkinter.StringVar(self)
            self.entry = tkinter.Entry(self, textvariable=self.textAnswer)
            self.entry.pack()
            
            self.submitButton = tkinter.Button(self, text="Submit Answer", command=self.submit)
            self.submitButton.place(x=0, y=50)
            self.mainloop()

        def submit(self):
            
            if self.textAnswer.get() == self.titleName:
                self.passed = True
                self.destroy()
                
class TextInput:
    
    def __init__(self, name, puzzleid = None, *args) -> None:
        
        match puzzleid:
            
            case 0:
                
                self.reversePuzzle(name)
                
            case 1:
                
                self.cypherPuzzle(name, args[0])
                
            case 2:
                    
                    self.deletePuzzle(name)
                
            case 3:
                pass
            
            case 4:
                 pass
                
            case 5:
                pass
                
            case 6:
                pass
                
            case 7:
                pass
                
            case 8:
                pass
                
            case 9:
                pass
                
            case 10:
                pass
                
            case 11:
                pass
                
            case 12:
                pass
                
            case 13:
                pass
                
            case 14:
                pass
                
            case 15:
                pass
    
    def deletePuzzle(self, name):
        
        i=0
        
        self.fileObj = open(name[i], "w")
        self.fileObj.close()
        
        while True:
            
            fileExists = os.path.isfile(f"{os.getcwd()}\\{name[i]}")
            
            if fileExists == False:
                
                i+=1
                
                if i == len(name):
                    return
                
                self.fileObj = open(name[i], "w")
                self.fileObj.close()
                
                

            time.sleep(0.5)
        
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
        self.fileObj.write("The answer to this puzzle requires an input of text into the terminal relating to the file, when you think you have the answer type it into the terminal,                                                                                                                                                                                                                                                                                                               Think Backwards")
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
            
        