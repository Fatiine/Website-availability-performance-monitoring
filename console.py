import sys,os
import curses



def draw_menu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen
    stdscr.clear()
    stdscr.refresh()

    # Initialize colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loop where k is the last character pressed
    while (k != ord('q')):

        # Declaration of strings
        statusbarstr = "Press 'q' to exit | STATUS BAR "



        '''Draw borders of the different columns'''
        height, width = stdscr.getmaxyx()
        stdscr.border()
        stdscr.vline(1, int(3 * height / 4), '|', int(width - 2))
        stdscr.vline(1, int(height / 4), '|', int(width - 2))
        stdscr.refresh()

        '''initialize the http monitor'''
        monitor_column = curses.newwin(int(height - 2), int(width / 4 - 1), 1, 1)
        _, t_x = monitor_column.getmaxyx()
        monitor_column.setscrreg(3,height - 5)
        monitor_column.idlok(True)
        monitor_column.scrollok(True)
        monitor_column.attron(curses.color_pair(1))
        monitor_column.attron(curses.A_BOLD)
        monitor_column.addstr(0, int(t_x / 2 - 4), "Monitor")
        monitor_column.hline(1, 0, '-', t_x)
        monitor_column.addstr(3, int(t_x / 2 - 4), "So you lost your trust  And you never should have You never should have But dont brea your backfsee thisBut don't answer"
                                                   " thatIn a bullet-proof vestWith the windows all closedll be doing my bestll see you soonk your back"
                                                   "So you lost your trust  And you never should have You never should have But dont brea your backfsee thisBut don't answer"
                                                   " thatIn a bullet-proof vestWith the windows all closedll be doing my bestll see you soonk your back"
                                                   "So you lost your trust  And you never should have You never should have But dont brea your backfsee thisBut don't answer"
                                                   " thatIn a bullet-proof vestWith the windows all closedll be doing my bestll see you soonk your back"
                                                   "So you lost your trust  And you never should have You never should have But dont brea your backfsee thisBut don't answer"
                                                   " thatIn a bullet-proof vestWith the windows all closedll be doing my bestll see you soonk your back"
                                                   "So you lost your trust  And you never should have You never should have But dont brea your backfsee thisBut don't answer"
                                                   " thatIn a bullet-proof vestWith the windows all closedll be doing my bestll see you soonk your back"
                                                   "So you lost your trust  And you never should have You never should have But dont brea your backfsee thisBut don't answer"
                                                   " thatIn a bullet-proof vestWith the windows all closedll be doing my bestll see you soonk your back"
                                                   "So you lost your trust  And you never should have You never should have But dont brea your backfsee thisBut don't answer"
                                                   " thatIn a bullet-proof vestWith the windows all closedll be doing my bestll see you soonk your back"
                                                   "So you lost your trust  And you never should have You never should have But dont brea your backfsee thisBut don't answer"
                                                   " thatIn a bullet-proof vestWith the windows all closedll be doing my bestll see you soonk your back"
                                                   "So you lost your trust  And you never should have You never should have But dont brea your backfsee thisBut don't answer"
                                                   " thatIn a bullet-proof vestWith the windows all closedll be doing my bestll see you soonk your back"
                                                   "So you lost your trust  And you never should have You never should have But dont brea your backfsee thisBut don't answer"
                                                   " thatIn a bullet-proof vestWith the windows all closedll be doing my bestll see you soonk your back"
                                                   "So you lost your trust  And you never should have You never should have But dont brea your backfsee thisBut don't answer"
                                                   " thatIn a bullet-proof vestWith the windows all closedll be doing my bestll see you soonk your back"
                                                   "So you lost your trust  And you never should have You never should have But dont brea your backfsee thisBut don't answer"
                                                   " thatIn a bullet-proof vestWith the windows all closedll be doing my bestll see you soonk your back"
                                                   "So you lost your trust  And you never should have You never should have But dont brea your backfsee thisBut don't answer"
                                                   " thatIn a bullet-proof vestWith the windows all closedll be doing my bestll see you soonk your back"
                                                   "So you lost your trust  And you never should have You never should have But dont brea your backfsee thisBut don't answer"
                                                   " thatIn a bullet-proof vestWith the windows all closedll be doing my bestll see you soonk your back"
                                                   "So you lost your trust  And you never should have You never should have But dont brea your backfsee thisBut don't answer"
                                                   " thatIn a bullet-proof vestWith the windows all closedll be doing my bestll see you soonk your back"
                                                   "So you lost your trust  And you never should have You never should have But dont brea your backfsee thisBut don't answer"
                                                   " thatIn a bullet-proof vestWith the windows all closedll be doing my bestll see you soonk your back"
                                                   "So you lost your trust  And you never should have You never should have But dont brea your backfsee thisBut don't answer"
                                                   " thatIn a bullet-proof vestWith the windows all closedll be doing my bestll see you soonk your back"
                                                   "So you lost your trust  And you never should have You never should have But dont brea your backfsee thisBut don't answer"
                                                   " thatIn a bullet-proof vestWith the windows all closedll be doing my bestll see you soonk your back"
                                                   "So you lost your trust  And you never should have You never should have But dont brea your backfsee thisBut don't answer"
                                                   " thatIn a bullet-proof vestWith the windows all closedll be doing my bestll see you soonk your back"
                                                   "So you lost your trust  And you never should have You never should have But dont brea your backfsee thisBut don't answer"
                                                   " thatIn a bullet-proof vestWith the windows all closedll be doing my bestll see you soonk your back"
                                                   "So you lost your trust  And you never should have You never should have But dont brea your backfsee thisBut don't answer"
                                                   " thatIn a bullet-proof vestWith the windows all closedll be doing my bestll see you soonk your back"
                                                   "So you lost your trust  And you never should have You never should have But dont brea your backfsee thisBut don't answer"
                                                   " thatIn a bullet-proof vestWith the windows all closedll be doing my bestll see you soonk your back"
                                                   "So you lost your trust  And you never should have You never should have But dont brea your backfsee thisBut don't answer"
                                                   " thatIn a bullet-proof vestWith the windows all closedll be doing my bestll see you soonk your back"
                                                   "So you lost your trust  And you never should have You never should have But dont brea your backfsee thisBut don't answer"
                                                   " thatIn a bullet-proof vestWith the windows all closedll be doing my bestll see you soonk your back"
                              )

        monitor_column.attroff(curses.color_pair(1))
        monitor_column.attroff(curses.A_BOLD)

        monitor_column.noutrefresh()

        '''Initialize the Statistics column'''
        stats_column = curses.newwin(int(height - 2), int(width / 2 - 1), 1,
                                           int(width / 4 + 1))
        _, a_x = stats_column.getmaxyx()
        stats_column.attron(curses.color_pair(1))
        stats_column.attron(curses.A_BOLD)
        stats_column.addstr(0, int(a_x / 2 - 2), "Stats")
        stats_column.hline(1, 0, '-', a_x)
        stats_column.attroff(curses.color_pair(1))
        stats_column.attroff(curses.A_BOLD)
        stats_column.noutrefresh()

        '''Initialize the Alerts column'''
        alert_column = curses.newwin(int(height - 2), int(width / 4 - 1), 1,
                                       int(3 * width / 4 + 1))
        _, s_x = alert_column.getmaxyx()
        alert_column.attron(curses.color_pair(1))
        alert_column.attron(curses.A_BOLD)
        alert_column.addstr(0, int(s_x / 2 - 5), "Alerts")
        alert_column.hline(1, 0, '-', s_x)
        alert_column.attron(curses.color_pair(1))
        alert_column.attron(curses.A_BOLD)
        alert_column.noutrefresh()

        # Rendering some text
        whstr = "Width: {}, Height: {}".format(width, height)
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering title


        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text

        stdscr.move(height - 2, width - 2)

        # Refresh the screen
        stdscr.refresh()
        # Wait for next input
        k = stdscr.getch()

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()