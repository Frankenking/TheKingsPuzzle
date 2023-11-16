import random
import assets
import windows
import time
import threading

class Program:
    
    def __init__(self) -> None:
        
        self.running = True
        self.threadMain = threading.Thread(target=self._main)
        self.exodus = threading.Thread(target=self._second)
        
    def _menu(self):
        self.threadMain.start()

    def _second(self):
        pass
    
    def _main(self):
        
        for _ in range(4):
            print(assets.storylines[_])
            time.sleep(1)
            
        self.exodus.start()
        if self._getUserInput() == "Exodus":
            print(assets.storylines[4])
        else:
            self._quit()
            
    def _getUserInput(self, type='str'):
        try:
            _ = input("\n-->")
            return _
        except:
            return self._getUserInput(type)
    
    def _quit(self):
        self.running = False
        return breakpoint
    
    
    def __str__(self) -> str:
        pass
    
    
if __name__ == '__main__':
    _program = Program()
    _program._menu()
    