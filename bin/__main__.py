
#folder imports
import assets, puzzles

#py imports
import os, multiprocessing, time, random, threading


class Program:
    
    def __init__(self) -> None:
        #instantiates the game
        self.Game()
        
    class Game:
        
        def __init__(self) -> None:
            
            #instantiates the menu
            self.menuData  = self.Menu()
            
            #sets default userposition
            self.userPos = [0,0]
            
            #checks if the user has quit
            if self.menuData.hasQuit:
                return
            
            #loading data
            print(f" SEED: {self.menuData.gameSettings['seed']}\n DIFFICULTY: {self.menuData.gameSettings['difficulty']}\n Loading...")
            time.sleep(1)
            self._os('cls')
            
            #used as a counter for some "story" text 
            self.storylineNumber:int = 0
            
            #sets the global seed
            random.seed(self.menuData.gameSettings.get('seed'))
            
            #calls the start to begin the game
            self._start()
        
        def _start(self):
            
            #prints the first 5 storylines
            for _ in range(5):
                print(assets.storylines[self.storylineNumber] + "\n-----------------")
                time.sleep(1)
                self._incStoryline()
            
            #chooses a random window name from a list of random words in another python file and then instantiates a window used for input
            passWindowName = assets.names[random.randint(0, len(assets.names)-1)]
            self.passWindow = puzzles.passwordWindow('100x100',  passWindowName, True)
            
            #if the correct word was inputed into the window then the game continues
            if self.passWindow.passed:
                
                print(assets.storylines[self.storylineNumber] + "\n------------------")
                self._os('pause')
                self._os('cls')

            #otherwise the game ends
            else:
                
                self._os('cls')
                print("\n" + assets.userFailureLines[random.randint(0, len(assets.userFailureLines))] + "\n")
                self._os('pause')
                return

            #coordinatemap and the actual map with its data
            self.coordinateMap = []
            self.mapObject = []
            
            #generates the dimensions of the map depending on the difficulty
            self.dimensions:list = self._generateDimensions(self.menuData.gameSettings['difficulty'])
            
            #generates the coordinate map using the dimensions
            for x in range(self.dimensions[0]):
                    for y in range(self.dimensions[1]):
                        self.coordinateMap.append(str(x) +","+ str(y))
            
            #starts at the first room (index0) and applies the data from the cooridnate map to each room
            index = 0
            for point in self.coordinateMap:
                self.mapObject.append(self.Room(point, index))
                index+=1
            
            #this just sets the room that the player must get to to win depending on the difficulty
            for room in self.mapObject:
                if getattr(room, "coordinates") == "4,4":
                    setattr(room, "isCompletionRoom", True)
                    break
                elif getattr(room, "coordinates") == "8,8":
                    setattr(room, "isCompletionRoom", True)
                    break
                    
            #sets the first room to completed
            self._roomAtrSet(0, 'c', True)
            
            #starts the main process loops forever until the game ends
            self._proc()
            
        def _proc(self) -> None: #main runtime game loop
            
            while True:
                
                #starting text telling the player what they can do and where they need to go
                print(f"You begin the puzzle with a Map that outlines the rooms you can go to...\n------------------\nYour Goal is to reach the final room at {self.coordinateMap[len(self.coordinateMap)-1]}")
                print(f"\nDECISIONS\n LOCATION\n MOVE\n SEED\n")
                
                #get the userinput and lowercase it
                userInput = self._getUserInput()
                userInput = userInput.lower()
                
                #match what they typed in a call the corresponding function
                match userInput:
                    
                    case "location":
                        self._os("cls")
                        print(f"You are at {self.userPos}")
                    
                    case "move":
                        self.Usermove()
                        
                    case "seed":
                        self._os("cls")
                        print(self.menuData.gameSettings["seed"])
                    
                    case _:
                        print("Invalid Option")
        
        def Usermove(self):
            
            #prompts for movement direction
            print("Direction you wish to move Left/Right/Up/Down")
            userInput = self._getUserInput()
            userInput = userInput.lower()
                    
            match userInput:
                
                case "up":
                    #applies a change in positive y to the userpos variable
                    if self._checkValidMove(0,1):
                        self.userPos[1] = self.userPos[1] +1
                    else:
                        print("Invalid Direction")
                        return
                        
                case "down":
                    #applies a change in negative y to the userpos variable
                    if self._checkValidMove(0,-1):
                        self.userPos[1] = self.userPos[1] -1
                    else:
                        print("Invalid Direction")
                        return
                        
                case "left":
                    #applies a change in negative x to the userpos variable
                    if self._checkValidMove(-1,0):
                        self.userPos[0] = self.userPos[0] -1
                    else:
                        print("Invalid Direction")
                        return
                        
                case "right":
                    #applies a change in positive x to the userpos variable
                    if self._checkValidMove(1,0):
                        self.userPos[0] = self.userPos[0] +1
                    else:
                        print("Invalid Direction")
                        return
                        
                case _:
                    self._os("cls")
                    print("Invalid Option")
                    return self.Usermove()
            
            #formats the position for the room so it doesnt cause an exception since rooms use a string for coordinates while the userPos variable uses a list, so just a concatination
            pos = f"{self.userPos[0]},{self.userPos[1]}"
            
            for room in self.mapObject:
                
                #for every room if the room matches the current coordinates, if it is the final room you win, if not completed it starts a new random puzzle 
                if getattr(room, 'coordinates') == pos:
                    
                    print(getattr(room, 'coordinates'), getattr(room, "isCompletionRoom"))
                    
                    if getattr(room, "isCompletionRoom"):
                            self._end()

                    if False == getattr(room, 'isCompleted'):
                        self._instancePuzzle(room)
                        self._roomAtrSet(getattr(room, 'roomNumber'), "c", True)
                        
        
        def _instancePuzzle(self, room):
            
            puzzleid = getattr(room, 'roomType')
            
            name = assets.names[random.randint(0, len(assets.names)-1)]
            
            match puzzleid:
                
                #PUZZLE ONE BACKWARDS
                case 0:
                    
                    roomPuzzle = puzzles.puzzleHandler(name, puzzleid)
                
                #PUZZLE TWO CYPHER
                case 1:
                    
                    roomPuzzle = puzzles.puzzleHandler(name, puzzleid, random.randint(0, 25))
                
                #PUZZLE THREE DELETE
                case 2:
                    
                    roomPuzzle = self._generateThread(puzzles.puzzleHandler, name, puzzleid)
                    roomPuzzle.start()
                    
                    while True:
                        print("Answer: ")
                        if self._getUserInput() == name:
                            break
                        else:
                            self._os("cls")
                            print("Wrong")
                    
                    for character in name:
                        try:
                            os.remove(character)
                        except:
                            pass
                    
                #PUZZLE FOUR TIMED DELETE
                case 3:
                    
                    wires = ["greenwire", "bluewire", "redwire", "yellowwire"]
                    wireindex =random.randint(0,3)
                    wire = wires[wireindex]
                    roomPuzzle = puzzles.puzzleHandler(name, puzzleid, wire, wires)
                    
        
                    for wireName in wires:
                        try:
                            os.remove(wireName)
                        except:
                            pass
                    
                    if roomPuzzle.passed == False:
                        print("GAME OVER")
                        self._os("pause")
                        exit()
                    
                #PUZZLE FIVE RIDDLES
                case 4:
                    
                    index = random.randint(0, 14)
                    riddle = assets.riddles[index]
                    ans = assets.riddleAnswers[index]
                    roomPuzzle = puzzles.puzzleHandler(name, puzzleid, riddle, ans)
                
                #PUZZLE SIX PATIENT
                case 5:
                    
                    roomPuzzle = puzzles.puzzleHandler(name, puzzleid)
                    
                #PUZZLE SEVEN LUCK
                case 6:
                    
                    roomPuzzle = puzzles.puzzleHandler(name, puzzleid)
                
                #PUZZLE EIGHT CODE
                case 7:
                    
                    roomPuzzle = puzzles.puzzleHandler(name, puzzleid, random.randint(0,9))
                
                case 8:
                    pass
                
                case 9:
                    pass
                
                case _:
                    print("Fatal Exception")
                    raise Exception
                
            self._os("cls")
            print("----------------Room Completed!----------------")
        
        def _checkValidMove(self, x=0, y=0) -> bool:
            
            #gets the rooms to go to
            targetRoom = []
            targetRoom.append(x+self.userPos[0])
            targetRoom.append(y+self.userPos[1])
            
            #if the target room is not within the bounds of the map then return false else true
            if targetRoom[0] < 0 or targetRoom[0] > 4*self.menuData.gameSettings["difficulty"] or targetRoom[1] < 0 or targetRoom[1] > 4*self.menuData.gameSettings["difficulty"]:
                return False
            else:
                return True
            
        def _roomAtrSet(self, roomnumber, type, val):
            
            #used for manipulating the room object attributes easily
            match type:
                
                case 'cR':
                    setattr(self.mapObject[roomnumber], 'isCompletionRoom', val)
                
                case 'c':
                    setattr(self.mapObject[roomnumber], 'isCompleted', val)
                    
        def _incStoryline(self) -> None: #progresses the lines that contribue to the story when called
            self.storylineNumber +=1
            
        def _getUserInput(self, type='str'): #input handler, deals with "complex" user interactions uses a type defaulted to string to ensure no crashes if the user mistypes or tries to break the program
            
            try:
                userInput = input("\nUser Input -->")
                self._os('cls')
                
                match type:
                    
                    case 'str':
                        return userInput
                    
                    case 'int':
                        return int(userInput)
                    
                    case 'float':
                        return float(userInput)
                        
            except:
                
                print("Invalid Character")
                return self._getUserInput(type)
                
        def _os(self, cmd): #allows easier syntax when managing terminal command inputs, cls, dir, cd, etc.
                os.system(cmd)
        
        def _generateThread(self, *args): #uses the first value in args (the target) in target= then takes everything after it as input if you want to uses variables in a method, class, etc. except its a thread 
            return threading.Thread(target=args[0], args=args[1:len(args)])
        
        def _generateDimensions(self, difficulty) -> list:
                x = 5*difficulty
                y = 5*difficulty
                return x, y
        
        #END FUNC-----------------------------------------------
        
        def _end(self):
            self._os("cls")
            print(f"You Won Congratulations!, Thank you for playing\n SEED: {self.menuData.gameSettings['seed']}\n DIFFICULTY: {self.menuData.gameSettings['difficulty']}")
            self._os("pause")
            quit()
            
        #ROOM CONSTRUCTOR ----------------------------------------------------------------------------------------------------------------------------------------------------
        
        class Room:
                
            def __init__(self, roomCoords, roomN) -> None:
                
                self.coordinates = roomCoords
                self.roomNumber = roomN
                self.isCompletionRoom = False
                self.isCompleted = False
                #self.roomType = random.randint(0, 9)
                self.roomType = random.randint(0,7)
                
        #MENU CLASS ----------------------------------------------------------------------------------------------------------------------------------------------------
                
        class Menu:
        
            def __init__(self)  -> None:
                
                self.gameSettings = {'seed': 0, 'difficulty':1}
                self.hasQuit = False
                
                print(assets.ascii[0])
                
                self._os('pause')
                self._os('cls')
                
                self._menu()
                
            def _menu(self) -> None: #Menu handles interactions before the game starts
                
                while not self.hasQuit:
                    print(f"{assets.ascii[1]} \n Type the words you see to access them Ex 'OPTIONS' \n\nSTART\nLOAD\nOPTIONS\nQUIT\nYou may want to visit OPTIONS first to customize your experience")
                    userInput = self._getUserInput()
                    userInput = userInput.upper()
                    
                    match userInput:
                        
                        case "START":
                            self._os('cls')
                            break
                        
                        case "OPTIONS":
                            self._os('cls')
                            self._gameOptions()
                        
                        case "QUIT":
                            self._quit()
                            self._os('cls')
                        
                        case _:
                            print("Invalid Request")
                            
            def _gameOptions(self) -> None: #options interface that takes user input and edits the gameSettings attribute before the Game is started
                
                back = False
                
                while not back:
                    
                    print(self.gameSettings)
                    
                    try:
                        
                        print(f"{assets.ascii[2]} \n Type the Option you wish to modify then in the next prompt the number value with the specified range, Ex 'DIFFICULTY' then '1' \n\nDIFFICULTY\nSEED\nBACK ")
                        userInput = self._getUserInput()
                        userInput = userInput.upper()
                        
                        match userInput:
                            
                            case "DIFFICULTY":
                                print("'1' for Normal\n'2' for Hard")
                                userInput = self._getUserInput("int")
                                
                                if userInput == 1 or userInput == 2:
                                    self.gameSettings["difficulty"] = userInput
                                    
                                else:
                                    print("Invalid Difficulty")
                                    return self._gameOptions()
                                
                            case "SEED":
                                print("This option determines the consistent randomness, Input any whole value Ex 1 or 200 or 1999 etc.")
                                userInput = self._getUserInput("int")
                                self.gameSettings["seed"] = userInput
                            
                            case "BACK":
                                return
                            
                            case _:
                                print("Invalid Request")
                                
                    except:
                        print("Invalid Request")
                        
            def _getUserInput(self, type='str'): #input handler, deals with "complex" user interactions uses a type defaulted to string to ensure no crashes if the user mistypes or tries to break the program
                
                try:
                    userInput = input("\nUser Input -->")
                    self._os('cls')
                    
                    match type:
                        
                        case 'str':
                            return userInput
                        
                        case 'int':
                            return int(userInput)
                        
                        case 'float':
                            return float(userInput)
                        
                except:
                    
                    print("Invalid Character")
                    return self._getUserInput(type)
            
            def _quit(self): #determines whether the user has quit or not, returns to master program instance which then ends the program
                print("Quiting...")
                time.sleep(1)
                self.hasQuit = True
                return
            
            def _os(self, cmd):
                os.system(cmd)

_program = Program()