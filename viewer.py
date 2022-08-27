from colorama import Fore, init
from os import walk
import json, threading, os
init()

####### COLORS #######
RED = Fore.LIGHTRED_EX
GREEN = Fore.LIGHTGREEN_EX
YELLOW = Fore.LIGHTYELLOW_EX
BLUE = Fore.LIGHTBLUE_EX
MAGENTA = Fore.LIGHTMAGENTA_EX
CYAN = Fore.LIGHTCYAN_EX
WHITE = Fore.LIGHTWHITE_EX
RESET = Fore.RESET

__LOCK__ = threading.Lock()
__NAME__ = "Valeria2001"

class Console:
    @staticmethod
    def printConvers(author: str, msg: str) -> None:
        __LOCK__.acquire()
        if author.lower() in ['me', __NAME__]:
            print(f'{WHITE}[{CYAN}+{WHITE}] {CYAN}{author}: {RESET}{msg}')
        if author.lower() == "image":
            print(f'{WHITE}[{MAGENTA}+{WHITE}] {MAGENTA}{author}: {RESET}{msg}')
        else:
            print(f'{WHITE}[{YELLOW}-{WHITE}] {YELLOW}{author}: {RESET}{msg}')
        __LOCK__.release()
    
    @staticmethod
    def printf(content: str, color: str, stop: bool = False):
        __LOCK__.acquire()
        print(f"\n{color}[{WHITE}·{color}] {content}{RESET}")
        if stop:
            input()
            os.system('cls' if os.name == 'nt' else 'clear')
        __LOCK__.release()

files = []
for (dirpath, dirnames, filenames) in walk("conversations"):
    files.extend(filenames)
    break

counter = 1
total = len(files)

for x in files:
    with open(f"conversations/{x}", "r", encoding="utf-8") as file:
        data = json.load(file)
    
    Console.printf(f"Conversación {counter}\n", GREEN)

    for y in data.values():
        Console.printConvers(y["author"], y["msg"])

    Console.printf(f"Press Enter for the next conversation ({counter}/{total})", MAGENTA, True)
    counter += 1