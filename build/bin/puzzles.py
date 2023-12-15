import tkinter, os, time, random
from tkinter import messagebox
from pynput import mouse

class passwordWindow(tkinter.Tk):
        
        def __init__(self, windowGeometry="0x0", windowTitle="None", iconifyWindow = False) -> None:
            super().__init__()
            self.passed = False #beat the puzzle or not
            self.titleName = windowTitle #name
            self.geometry(windowGeometry) #dims
            
            if iconifyWindow:
                self.iconify() #minimize
                
            self.title(windowTitle) #titl
            
            self.textAnswer = tkinter.StringVar(self) #entry box for answer
            self.entry = tkinter.Entry(self, textvariable=self.textAnswer)
            self.entry.pack()
            
            self.submitButton = tkinter.Button(self, text="Submit Answer", command=self.submit) #submit answer
            self.submitButton.place(x=0, y=50)
            self.mainloop()

        def submit(self):
            
            if self.textAnswer.get() == self.titleName:
                self.passed = True #if you got it right you beat it...
            
            self.destroy()
    
class patientPuzzle:
    
    def __init__(self) -> None:
        self.mouseListener = mouse.Listener(on_move=self.on_move)
        self.mouseListener.start() #listen for mouse movement
        self.secondCount = 0
        
        #count every second the user has not move their mouse
        while True:
            time.sleep(1)
            self.secondCount+=1
            if self.secondCount >= 30:
                self.mouseListener.stop()
                break
    
    #if they moved it reset it
    def on_move(self, x, y):
        self.secondCount = 0

#alot of these classes could use cleanup but im not going to touch anything for now

class bombPuzzle:
    
    def __init__(self, wire, wires) -> None:
        super().__init__()
        
        self.passed = False
        messagebox.showinfo("", f"cut the {wire}") #tells the user which wire to cut
        
        for i in wires:
            #generate wire files
            fileObj = open(i, "w")
            fileObj.close()
        
        for i in range(0, 30):
            #count down from 30
            for g in range(0,4):
                #check for every file wire if it exists in the cwd
                fileExists = os.path.isfile(f"{os.getcwd()}\\{wires[g]}")
                
                if fileExists == False and wires[g] == wire:
                    self.passed = True
                    return
                    
                elif fileExists == False:
                    self.passed = False
                    return
            
            print(f"{30-i} seconds left")
            time.sleep(1)
        
        #;(
        self.passed = False
        
class puzzleHandler:
    
    #class for handling all the functions and proccess for the puzzles and making them do things and stuff
    def __init__(self, name, puzzleid = None, *args) -> None:
        
        self.passed = False #variable used to check if they actually beat the puzzle or not
        
        match puzzleid:
            
            #match every puzzle id to the corresponding class/method
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
                
                self.colorPuzzle(name, args[0])
                
            case 9:
                
                self.binaryPuzzle(name)
                
    def _editPuzzle(self, name):
        
        #generate file
        messagebox.showinfo(name, "luck is not with you")
        fileobj = open(name, "w")
        fileobj.write("100")
        fileobj.close()
        
        while True:
            
            #this puzzle is rigged against the player in an impossible coin flip, unless they change the chance which is pulled from the generated file
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
        
        #starts the patient puzzle and instances the class
        messagebox.showinfo(name, "The key is patience")
        _patient_puzzleMinigame = patientPuzzle()
    
    def deletePuzzle(self, name):
        
        #the user must delete each file one after another a new one every time, each file being named sequetially a letter of the answer
        
        i=0
        
        fileObj = open(name[i], "w") #create first file
        fileObj.close()
        
        while True:
            
            fileExists = os.path.isfile(f"{os.getcwd()}\\{name[i]}") #check while current file not deleted if it does exsists make the next one
            
            if fileExists == False:
                
                i+=1
                
                if i == len(name): #end if no more letters left to make
                    return
                
                fileObj = open(name[i], "w")
                fileObj.close()

            time.sleep(0.5)
        
    def cypherPuzzle(self, name, key):
        
        #encrypts a word using a random key in a caesarcypher
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
        #the user must type the name of the file backwards into the command terminal
        
        fileObj = open(name, 'w')
        fileObj.write("The answer to this puzzle requires an input of text into the terminal relating to the file, when you think you have the answer type it into the terminal,                                                                                                                                                                                                                                                                                                               Think Backwards")
        fileObj.close()
        
        listname = []
        for i in name: # make a new list of all the letters
            listname.append(i)
        listname = listname[::-1] #INVERT
        invname = ''.join(listname) #then join into a string again i could've just used a built in python function but I think its better to practice and problem solve yourself
        
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
        
        #funny little one where the user has to solve a simple coding problem
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
        
    def colorPuzzle(self, name, randint):
            
        fileobj = open(name, "w")
        #depending on the randominteger write a color RGB in the textfile then ask them for the corresponding color name
        match randint:
            case 0:
                fileobj.write("255,0,0")
                answer = "red"
            case 1:
                fileobj.write("0,255,0")
                answer = "green"
            case 2:
                fileobj.write("0,0,255")
                answer = "blue"
            
        fileobj.close()
            
        while True:
            userInput = input("Answer: ")
            userInput = userInput.lower()
            if userInput == answer:
                os.remove(name)
                return
            else:
                print("Wrong")
        
    def binaryPuzzle(self, name):
        
        
        fileobj = open("file", "w")
        
        #turn it into unicode then convert unicode to binary and reassign it to binaryName
        temp = name
        l,m=[],[]
        for i in temp:
            l.append(ord(i))
        for i in l:
            m.append(str(bin(i)[2:]))
        temp = m
        
        binaryName = ''.join(temp)
        
        fileobj.write(binaryName)
        fileobj.close()
        
        #wait for answer
        while True:
            userInput = input("Answer: ")
            if userInput == name:
                try:
                    os.remove("file")
                except:
                    pass
                return
            else:
                print("Wrong")