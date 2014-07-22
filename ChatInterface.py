import curses

# A chat window to complement chat-client.py.
# GOALS:
# (1): three main frames ...
#      - display received text
#      - display own user input to be sent to stdin
#      - display connected users
# (2): color support
#      - colors to distinguish user aliases
#      - colors to distinguish emotes, whispers, special commands
#        that are not part of the 'chat'

TOP_BORDER_Y = 1
TOP_BORDER_X = 0
CHAT_HEIGHT = 20
CHAT_WIDTH = 70
CHAT_X = 2
CHAT_Y = 4
INPUT_HEIGHT = 1
INPUT_WIDTH = 70
INPUT_Y = 35
INPUT_X = 2


class ChatInterface:
    def __init__(self):
        # Initialize the screen and three sub-windows (chat, input, users).
        self.screen = curses.initscr()
        self.screen.hline(TOP_BORDER_Y,TOP_BORDER_X,curses.ACS_HLINE,curses.COLS)

        # THE FOLLOWING IS FOR CHATWINDOW
        self.screen.hline(3,1,curses.ACS_HLINE,curses.COLS-25) # Top Border
        self.screen.hline(3,1,curses.ACS_ULCORNER,1) # Upper-Left Corner
        self.screen.hline(3,curses.COLS-25,curses.ACS_URCORNER,1) # Upper-Right Corner
        self.screen.vline(4,1,curses.ACS_VLINE,curses.LINES-7) # Left Border
        self.screen.vline(4,curses.COLS-25,curses.ACS_VLINE,curses.LINES-7) # Right Border
        self.screen.hline(curses.LINES-7,1,curses.ACS_HLINE,curses.COLS-25) # Bottom Border
        self.screen.hline(curses.LINES-7,1,curses.ACS_LLCORNER,1) # Bottom-left Border
        self.screen.hline(curses.LINES-7,curses.COLS-25,curses.ACS_LRCORNER,1) # Bottom-right Border

        # THE FOLLOWING IS FOR INPUTWINDOW
        self.screen.hline(curses.LINES-6,1,curses.ACS_HLINE,curses.COLS-25) # Top Border
        self.screen.hline(curses.LINES-6,1,curses.ACS_ULCORNER,1) # Upper-Left Corner
        self.screen.hline(curses.LINES-6,curses.COLS-25,curses.ACS_URCORNER,1) # Upper-Right Corner
        self.screen.vline(curses.LINES-5,1,curses.ACS_VLINE,1) # Left Border
        self.screen.vline(curses.LINES-5,curses.COLS-25,curses.ACS_VLINE,1) # Right Border
        self.screen.hline(curses.LINES-4,1,curses.ACS_HLINE,curses.COLS-25) # Bottom Border
        self.screen.hline(curses.LINES-4,1,curses.ACS_LLCORNER,1) # Bottom-left Border
        self.screen.hline(curses.LINES-4,curses.COLS-25,curses.ACS_LRCORNER,1) # Bottom-right Border

        self.screen.addstr(0,curses.COLS/2 - 30, "The Super-Fantastic LizChat 1.0") # Clever title
        self.chatWindow = curses.newwin(curses.LINES-11,curses.COLS-27,CHAT_Y,2) # Chat Window
        self.inputWindow = curses.newwin(1,curses.COLS-27,curses.LINES-5,2) # Input Window
       
        self.chatWindow.scrollok(True)
 
        self.screen.refresh()
        self.chatWindow.refresh()
        self.inputWindow.refresh()

    def _close(self):
        curses.endwin() 

def main():
    running = 1
    myScreen = ChatInterface()
    while running == 1:
        c = myScreen.inputWindow.getstr(0,0,140)
        if c == "/quit":
            running = 0
            break
        myScreen.chatWindow.addstr("Liz: ")
        myScreen.chatWindow.addstr(c)
        myScreen.chatWindow.addstr("\n")
        myScreen.inputWindow.clrtoeol()
        myScreen.chatWindow.refresh()
        myScreen.inputWindow.refresh()
    myScreen._close()
 
if __name__ == '__main__':
    main()
