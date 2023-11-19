
#folder imports
import assets
import externals

#py imports
import os, threading, time, random, math


class Program:
    
    def __init__(self) -> None:
        
        self.programRunning = True

        self.threadMain = threading.Thread(target=self.Game, args=[self.programRunning])
        self.threadMain.run()
        
    
    
    class Game:
        
        def __init__(self, *args) -> None:
            
            self.programRunning:bool = args[0]
            
            self.menuData  = self.Menu()
            
            if self.menuData.hasQuit:
                return None
            
            self.storylineNumber:int = 0
            random.seed(self.menuData.gameSettings.get('seed'))
            
            
            self._start()
        
        def _start(self):
            
            for _ in range(4):
                print(assets.storylines[self.storylineNumber] + "\n-----------------")
                time.sleep(1)
                self.incStoryline()
                
            if self._getUserInput() == "Exodus":
                self.incStoryline()
                print(assets.storylines[self.storylineNumber] + "\n------------------")
                self._os('pause')
                self._os('cls')

            else:
                
                self._os('cls')
                print("\n" + assets.userFailureLines[random.randint(0, 4)] + "\n")
                self._os('pause')
                return
        
        def _proc(self) -> None:
            pass
        
        def incStoryline(self) -> None:
            self.storylineNumber +=1
            
        def _getUserInput(self, type='str'):
            try:
                _ = input("\nUser Input -->")
                return _
            except:
                return self._getUserInput(type)
            
        def _os(self, arg):
                os.system(arg)
            
            
        class Menu:
        
            def __init__(self)  -> None:
                
                self.gameSettings = {'seed': 0, 'difficulty':1}
                self.hasQuit = False
                
                
                
                print(assets.ascii[0])
                
                self._os('pause')
                self._os('cls')
                
                self._menu()
                
            def _menu(self) -> None:
                
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
                            
            
            def _gameOptions(self) -> None:
                back = False
                while not back:
                    try:
                        print(f"{assets.ascii[2]} \n Type the Option then a space then a number with the given range, Ex 'Difficulty 1' or 'Difficulty 2'\n ")
                        self._getUserInput()
                    except:
                        print("Invalid Request")
            
            def _getUserInput(self, type='str'):
                try:
                    _ = input("\nUser Input -->")
                    self._os('cls')
                    return _
                except:
                    self._os('cls')
                    print("Error!")
                    return self._getUserInput(type)
            
            def _load(self):
                pass
            
            def _quit(self):
                print("Quiting...")
                time.sleep(1)
                self.hasQuit = True
                return
            
            def _os(self, arg):
                os.system(arg)
                
    def __str__(self) -> str:
        pass
    
    
if __name__ == '__main__':
    _program = Program()
    