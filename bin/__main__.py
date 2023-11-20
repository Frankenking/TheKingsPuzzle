
#folder imports
import assets, externals

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
                self.incStoryline()
            
            passWindowName = assets.windowNames[random.randint(0, len(assets.windowNames)-1)]
            self.passWindow = self._generateThread(externals.WindowHandler, '0x0',  passWindowName, True)
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

            self.MapObject = self.MapGenerator(self.menuData.gameSettings['difficulty'])
            
            self.formattedMap = []
            for i in range(0, len(self.MapObject.map)):
                self.formattedMap.append(str(self.MapObject._getDataRoomData(i)))
                
            print(self.formattedMap)
            
            
            self._proc()
            
        def _proc(self) -> None: #main runtime game loop
            
            while self.programRunning:
                print(f"You begin the puzzle with a Map that outlines the rooms you can go to...\n------------------\nYour Goal is to reach the final room at {str(self.MapObject._getDataRoomData(len(self.MapObject.map)-1))}")
                self._os('pause')
                
        
        def incStoryline(self) -> None: #progresses the lines that contribue to the story when called
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
            
        class MapGenerator:
            
            def __init__(self, difficulty) -> None:
                
                self.dimensions:list = self._generateDimensions(difficulty)
                self.map = []
                for x in range(self.dimensions[0]):
                    for y in range(self.dimensions[1]):
                        self.map.append(str(x) +","+ str(y))
                
                completionRoomNumber = len(self.map)
                count = 0
                for room in self.map:
                    room = self.Room(room, count)
                    if count == completionRoomNumber:
                        room.isCompletionRoom = True
                        
                    self.map[count] = room
                    
                    count +=1
                    
            def _generateDimensions(self, difficulty) -> list:
                x = 5*difficulty
                y = 5*difficulty
                return x, y
            
            def _getDataRoomData(self, roomNumber):
                return self.map[roomNumber]
                    
                    
            
            class Room:
                
                def __init__(self, roomCoords, roomN) -> None:
                    self.coordinates = roomCoords
                    self.roomNumber = roomN
                    self.isCompletionRoom = False

                def __str__(self) -> str:
                    return str(self.coordinates)
                
if __name__ == '__main__':
    _program = Program()