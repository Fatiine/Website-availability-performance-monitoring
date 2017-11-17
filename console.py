import sys, os
import curses
from website import Website
from monitor import Monitor
from database import create_tables
import time
from termcolor import colored





def draw_menu():
    # Test Monitor
    m = Monitor()
    w = Website("http://yahoo.fr", 2)
    w2 = Website("http://enpc.fr/", 3)
    w3 = Website("http://ecodomemroc.com/", 4)

    m.add_website(w)
    m.add_website(w2)

    create_tables('monitor.db')
    m.run_monitor('monitor.db')

    line = m.statsPrinter('monitor.db', 10, 5)
    line2 = m.alertsPrinter('monitor.db', 10)
    k = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen
    stdscr = curses.initscr()
    stdscr.clear()
    stdscr.refresh()

    # Initialize colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.curs_set(0)
    # Loop where k is the last character pressed
    while (k != ord('q')):
        # Declaration of strings
        statusbarstr = "Press 'q' to exit | STATUS BAR "

        '''Draw borders of the different columns'''
        height, width = stdscr.getmaxyx()
        stdscr.border()
        stdscr.vline(1, 3 * height // 4, '|', width - 2)
        stdscr.vline(1, height // 4, '|', width - 2)
        stdscr.refresh()

        '''Initialize the Statistics column'''
        stats_column = curses.newwin(height - 2, 3 * width // 4, 1,
                                     1)
        _, a_x = stats_column.getmaxyx()
        stats_column.attron(curses.color_pair(1))
        stats_column.attron(curses.A_BOLD)
        stats_column.addstr(0, a_x // 2 - 2, "Statistiques")
        stats_column.hline(1, 0, '-', a_x)
        stats_column.attroff(curses.color_pair(1))
        stats_column.attroff(curses.A_BOLD)

        stats_column.addstr(3, 1, line)

        stats_column.noutrefresh()

        '''Initialize the Alerts column'''
        alert_column = curses.newwin(height - 2, width // 4, 1,
                                     3 * width // 4)
        _, s_x = alert_column.getmaxyx()
        alert_column.attron(curses.color_pair(1))
        alert_column.attron(curses.A_BOLD)
        alert_column.addstr(0, s_x // 2 - 5, "Alerts")
        alert_column.hline(1, 0, '-', s_x)
        alert_column.attroff(curses.color_pair(1))
        alert_column.attroff(curses.A_BOLD)

        alert_column.attron(curses.color_pair(2))
        alert_column.addstr(3, s_x // 2 - 5, line2)
        alert_column.attroff(curses.color_pair(2))

        alert_column.noutrefresh()

        # Rendering some text
        whstr = "Width: {}, Height: {}".format(width, height)
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height - 1, 0, statusbarstr)
        stdscr.addstr(height - 1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
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

def draw_menu_loop():
    while True:
        draw_menu()
        curses.napms(10000)
def main():
    curses.wrapper(draw_menu_loop())


if __name__ == "__main__":
    main()