import os
import time

# ANSI color styles for terminal (foreground + background)
styles = [
    {"name": "White on Black", "fg": "\033[97m", "bg": "\033[40m"},
    {"name": "Black on Yellow", "fg": "\033[30m", "bg": "\033[103m"},
    {"name": "Black on White", "fg": "\033[30m", "bg": "\033[107m"},
    {"name": "Yellow on Blue", "fg": "\033[93m", "bg": "\033[44m"},
    {"name": "Bright Green on Black", "fg": "\033[92m", "bg": "\033[40m"},
]


RESET = "\033[0m"
BOLD = "\033[1m"


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    sample_text = "SAMPLE TEXT"

    clear_screen()

    print("HIGH-CONTRAST TEXT DISPLAY TEST\n")

    for style in styles:
        print(f"{style['bg']}{style['fg']}{BOLD}== {style['name']} =={RESET}")
        print(f"{style['bg']}{style['fg']} {sample_text} {RESET}")
        time.sleep(0.5)

if __name__ == "__main__":
    main()