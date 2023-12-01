
#folder imports
import assets, puzzles

#py imports
import os, multiprocessing, time, random, math


class Program:
    
    def __init__(self) -> None:
        
        self.programRunning = True

        self.Game(self.programRunning)
        
    class Game:
        
        def __init__(self, *args) -> None:
            
            self.PROGRAMVARS = args
            
            self.programRunning:bool = self.PROGRAMVARS[0]
            
            self.menuData  = self.Menu()
            self.userPos = "0,0"
            
            if self.menuData.hasQuit:
                return
            
            print(f" SEED: {self.menuData.gameSettings['seed']}\n DIFFICULTY: {self.menuData.gameSettings['difficulty']}\n Loading...")
            time.sleep(1)
            self._os('cls')
            
            self.storylineNumber:int = 0
            random.seed(self.menuData.gameSettings.get('seed'))
            
            
            self._start()
        
        def _start(self):
            
            for _ in range(4):
                print(assets.storylines[self.storylineNumber] + "\n-----------------")
                time.sleep(1)
                self._incStoryline()
            
            passWindowName = assets.windowNames[random.randint(0, len(assets.windowNames)-1)]
            self.passWindow = self._generateThread(puzzles.WindowHandler, '0x0',  passWindowName, True)
            self.passWindow.start()
            
            
            if self._getUserInput() == passWindowName:
                self.passWindow.terminate()
                print(assets.storylines[self.storylineNumber] + "\n------------------")
                self._os('pause')
                self._os('cls')

            else:
                
                self._os('cls')
                print("\n" + assets.userFailureLines[random.randint(0, len(assets.userFailureLines))] + "\n")
                self._os('pause')
                return

            self.coordinateMap = []
            self.mapObject = []
            
            self.dimensions:list = self._generateDimensions(self.menuData.gameSettings['difficulty'])
            
            for x in range(self.dimensions[0]):
                    for y in range(self.dimensions[1]):
                        self.coordinateMap.append(str(x) +","+ str(y))
            
            index = 0
            for point in self.coordinateMap:
                self.mapObject.append(self.Room(point, index))
                index+=1
                
                
            self._proc()
            
        def _proc(self) -> None: #main runtime game loop
            
            while self.programRunning:
                    
                print(f"You begin the puzzle with a Map that outlines the rooms you can go to...\n------------------\nYour Goal is to reach the final room at {self.coordinateMap[len(self.coordinateMap)-1]}")
                print(f"\nDECISIONS\n LOCATION\n MOVE\n")
                userInput = self._getUserInput()
                userInput = userInput.lower()
                
                match userInput:
                    
                    case "location":
                        self._os("cls")
                        print(f"You are at {self.userPos}")
                    
                    case "move":
                        self.Usermove()
                    
                    case _:
                        print("Invalid Option")
                
        def Usermove(self):
            print("Direction you wish to move Left/Right/Up/Down")
            userInput = self._getUserInput()
            userInput = userInput.lower()
            
            match userInput:
                case "up":
                    if self._checkValidMove(0,1):
                        self.userPos[1] = self.userPos[1] +1
                    else:
                        print("Invalid Direction")
                        
                case "down":
                    if self._checkValidMove(0,-1):
                        self.userPos[1] = self.userPos[1] -1
                    else:
                        print("Invalid Direction")
                        
                case "left":
                    if self._checkValidMove(-1,0):
                        self.userPos[0] = self.userPos[0] -1
                    else:
                        print("Invalid Direction")
                        
                case "right":
                    if self._checkValidMove(1,0):
                        self.userPos[0] = self.userPos[0] +1
                    else:
                        print("Invalid Direction")
                        
                case _:
                    self._os("cls")
                    print("Invalid Option")
                    return self.Usermove()
            
            
        def _checkValidMove(self, x=0, y=0) -> bool:
            
            targetRoom = []
            targetRoom.append(x+self.userPos[0])
            targetRoom.append(y+self.userPos[1])
            
            if targetRoom[0] < 0 or targetRoom[0] > 4*self.menuData.gameSettings["difficulty"]:
                return False
            
            
        def _incStoryline(self) -> None: #progresses the lines that contribue to the story when called
            self.storylineNumber +=1
            
        def _getUserInput(self, type='str'): #input handler, deals with "complex" user interactions
            
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
                
        def _os(self, cmd):
                os.system(cmd)
        
        def _generateThread(self, *args):  #uses the first value in args (the target) in target= then takes everything after it as input if you want to uses variables in a method, class, etc.
            return multiprocessing.Process(target=args[0], args=args[1:len(args)])
        
        def _generateDimensions(self, difficulty) -> list:
                x = 5*difficulty
                y = 5*difficulty
                return x, y
            
        class Room:
                
            def __init__(self, roomCoords, roomN) -> None:
                self.coordinates = roomCoords
                self.roomNumber = roomN
                
                if roomN == 25 or roomN == 50:
                    self.isCompletionRoom = False
                
                if roomCoords == '0,0':
                    self.isCompleted = True
                    self.isActive = True
                else:
                    self.isCompleted = False
                    self.isActive = False
            
            def _generatePuzzle(self):
                self.roomType = random.randint(0, 1)
                
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
                        
                        
            def _getUserInput(self, type='str'): #input handler, deals with "complex" user interactions
                
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
            
            def _load(self):
                pass
            
            def _quit(self):
                print("Quiting...")
                time.sleep(1)
                self.hasQuit = True
                return
            
            def _os(self, cmd):
                os.system(cmd)
            
                    
if __name__ == '__main__':
    _program = Program()