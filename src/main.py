import os
import time

RESET = "\033[0m" # default text attributes

# ANSI color styles dict: (name, foreground, background)
styles = [
    {"name": "Black on Blue",     "fg": "\033[104m", "bg": "\033[44m"},
    {"name": "Black on Cyan",     "fg": "\033[106m", "bg": "\033[30m"},
    {"name": "Black on Green",    "fg": "\033[102m", "bg": "\033[30m"},
    {"name": "Black on Magenta",  "fg": "\033[30m",  "bg": "\033[105m"},
    {"name": "Black on Red",      "fg": "\033[30m",  "bg": "\033[101m"},
    {"name": "Black on White",    "fg": "\033[107m", "bg": "\033[30m"},
    {"name": "Black on Yellow",   "fg": "\033[30m",  "bg": "\033[103m"},
    {"name": "Blue on Black",     "fg": "\033[94m",  "bg": "\033[40m"},
    {"name": "Blue on White",     "fg": "\033[94m",  "bg": "\033[107m"},
    {"name": "Blue on Yellow",    "fg": "\033[94m",  "bg": "\033[103m"},
    {"name": "Cyan on Black",     "fg": "\033[96m",  "bg": "\033[40m"},
    {"name": "Cyan on White",     "fg": "\033[96m",  "bg": "\033[107m"},
    {"name": "Green on Black",    "fg": "\033[92m",  "bg": "\033[40m"},
    {"name": "Green on White",    "fg": "\033[92m",  "bg": "\033[107m"},
    {"name": "Magenta on Black",  "fg": "\033[95m",  "bg": "\033[40m"},
    {"name": "Magenta on White",  "fg": "\033[95m",  "bg": "\033[107m"},
    {"name": "Red on Black",      "fg": "\033[91m",  "bg": "\033[40m"},
    {"name": "Red on White",      "fg": "\033[91m",  "bg": "\033[107m"},
    {"name": "Red on Yellow",     "fg": "\033[91m",  "bg": "\033[103m"},
    {"name": "White on Black",    "fg": "\033[97m",  "bg": "\033[40m"},
    {"name": "White on Blue",     "fg": "\033[97m",  "bg": "\033[44m"},
    {"name": "White on Cyan",     "fg": "\033[97m",  "bg": "\033[46m"},
    {"name": "White on Green",    "fg": "\033[97m",  "bg": "\033[42m"},
    {"name": "White on Magenta",  "fg": "\033[97m",  "bg": "\033[45m"},
    {"name": "White on Red",      "fg": "\033[97m",  "bg": "\033[41m"},
    {"name": "Yellow on Black",   "fg": "\033[40m",  "bg": "\033[93m"},
    {"name": "Yellow on Blue",    "fg": "\033[93m",  "bg": "\033[44m"},
    {"name": "Yellow on Magenta", "fg": "\033[93m",  "bg": "\033[45m"},
]

def clear_screen():
    # account for windows NT and unix
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    sample_text = "SAMPLE TEXT"
    clear_screen()

    for style in styles:
        """
        example of literal without f-string expressions:
        \033[30m\033[107m==Black on White ==\033[0m
        \033[30m\033[107mSAMPLE TEXT\033[0m
        $(ESCAPE->FG)$(ESCAPE->BG)$(YOUR_TEXT)$(ESCAPE_RESET)
        """

        print(f"{style['fg']}{style['bg']}=={style['name']}=={RESET}")
        print(f"{style['fg']}{style['bg']}{sample_text}{RESET}")

if __name__ == "__main__":
    main()