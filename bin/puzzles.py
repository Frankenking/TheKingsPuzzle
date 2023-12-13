import tkinter, os, time, random
from tkinter import messagebox
from pynput import mouse

class passwordWindow(tkinter.Tk):
        
        def __init__(self, windowGeometry="0x0", windowTitle="None", iconifyWindow = False) -> None:
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
    
class patientPuzzle:
    
    def __init__(self) -> None:
        self.mouseListener = mouse.Listener(on_move=self.on_move)
        self.mouseListener.start()
        self.secondCount = 0
        
        while True:
            time.sleep(1)
            self.secondCount+=1
            if self.secondCount >= 30:
                self.mouseListener.stop()
                break
    
    def on_move(self, x, y):
        self.secondCount = 0

class bombPuzzle:
    
    def __init__(self, wire, wires) -> None:
        super().__init__()
        
        self.wires = wires
        self.wire = wire
        self.passed = False
        messagebox.showinfo("", f"cut the {self.wire}")
        
        for i in wires:
            fileObj = open(i, "w")
            fileObj.close()
        
        for i in range(0, 30):
            
            for g in range(0,4):
                
                fileExists = os.path.isfile(f"{os.getcwd()}\\{self.wires[g]}")
                
                if fileExists == False and self.wires[g] == self.wire:
                    print("nex, iswire, Check Passed")
                    self.passed = True
                    return
                    
                elif fileExists == False:
                    self.passed = False
                    return
            
            print(f"{30-i} seconds left")
            time.sleep(1)
        
        self.passed = False
        
class puzzleHandler:
    
    def __init__(self, name, puzzleid = None, *args) -> None:
        
        self.fileToDelete = ""
        self.passed = False
        
        match puzzleid:
            
            case 0:
                
                self.reversePuzzle(name)
                
            case 1:
                
                self.cypherPuzzle(name, args[0])
                
            case 2:
                    
                self.deletePuzzle(name)
                
            case 3:
                
                self.bombMinigame(args[0], args[1])
                
            case 4:
                
                self.riddlePuzzle(args[0], args[1])
                
            case 5:
                
                self._patientPuzzle(name)
                
            case 6:
                
                self._editPuzzle(name)
                
            case 7:
                
                self.codePuzzle(args[0])
                
            case 8:
                pass
                
            case 9:
                pass
                
    def _editPuzzle(self, name):
        
        messagebox.showinfo(name, "luck is not with you")
        fileobj = open(name, "w")
        fileobj.write("100")
        fileobj.close()
        
        while True:
            
            print("Type flip to flip a coin, you must flip heads to win")
            userInput = input("Flip a coin: ")
            userInput = userInput.lower()
            
            try:
                fileobj = open(f"{os.getcwd()}\\{name}", "r")
                data = int(fileobj.read())
            except:
                print("dont type words please")
                userInput = ""
                fileobj.close()
            
            if userInput == "flip":
                if random.randint(0, 100) > data:
                    fileobj.close()
                    os.remove(f"{os.getcwd()}\\{name}")
                    break
                else:
                    os.system("cls")
                    print("tails")
                    fileobj.close()
            else:
                os.system("cls")
    
    def _patientPuzzle(self, name):
        
        messagebox.showinfo(name, "The key is patience")
        _patient_puzzleMinigame = patientPuzzle()
    
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
        
    def bombMinigame(self, wire, wires):
        
        self.passed = False
        self._bomb = bombPuzzle(wire, wires)
        self.passed = self._bomb.passed

    def riddlePuzzle(self, riddle, ans):
        
        print(riddle)
        userInput = input("Answer: ")
        userInput = userInput.lower()
        
        if userInput != ans:
            os.system("cls")
            print("Wrong")
            return self.riddlePuzzle(riddle, ans)
    
    def codePuzzle(self, randint):
        
        x = 2
        y = ["1", 2, 4, True, False, 8, "x", x, "object", 1220]
        print(f"""
              
            What is the Output of this code? :
              
            x = 2
            y = ["1", 2, 4, True, False, 8, "x", x, "object", 1220]
            
            return str(y[{randint}])
              """)
        
        while True:
            userInput = input("Answer: ")
            if userInput == str(y[randint]):
                break
            else:
                print("Wrong")
        