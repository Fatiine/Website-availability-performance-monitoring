import sys, os
import curses
from website import Website
from monitor import Monitor
from database import create_tables
import time
from termcolor import colored
import threading


def displayConsole(displayTime,hourCheck, monitor):

    line = monitor.statsPrinter('monitor.db', displayTime, hourCheck)
    line2 = monitor.alertsPrinter('monitor.db', displayTime)

    k = 0

    # Clear and refresh the screen
    stdscr = curses.initscr()
    stdscr.clear()
    stdscr.refresh()

    # Initialize colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    # curses.curs_set(0)

    while (k != ord('q')):
        # Declaration of strings
        statusbarstr = "Press 'q' to exit  "

        '''Draw borders of the different columns'''
        height, width = stdscr.getmaxyx()
        stdscr.border()
        # stdscr.vline(1, 3 * height // 4, '|', width - 2)
        # stdscr.vline(1, height // 4, '|', width - 2)
        stdscr.refresh()

        '''Initialize the Statistics column'''
        stats_column = curses.newwin(height - 2, width // 2, 1,
                                     1)
        _, a_x = stats_column.getmaxyx()
        stats_column.scrollok(True)
        stats_column.attron(curses.color_pair(1))
        stats_column.attron(curses.A_BOLD)
        stats_column.addstr(0, a_x // 2 - 2, "Statistiques")
        stats_column.hline(1, 0, '-', a_x)
        stats_column.attroff(curses.color_pair(1))
        stats_column.attroff(curses.A_BOLD)

        stats_column.addstr(3, 1, line)

        stats_column.noutrefresh()

        '''Initialize the Alerts column'''
        alert_column = curses.newwin(height - 2, width // 2, 1,
                                     width // 2)
        _, s_x = alert_column.getmaxyx()
        alert_column.scrollok(True)
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
        return k


def menu(monitor):
    os.system('clear')
    choice = '0'
    while choice == '0':
        print("\033[95m Welcome to the Website availability & performance monitoring console application \033[0m")
        print("1 - Enter the website adresses to check and their check intervals")
        print("2 - Run the test")
        print("3 - Run the application")

        choice = input("\t\tPlease make a choice: ")

        if choice == "1":
            sub_menu1(monitor)

        elif choice == "2":
            print("Run the test")

        elif choice == "3":
            break

        else:
            print("I don't understand your choice.")
            menu(monitor)
        return

def sub_menu1(monitor):
    os.system('clear')
    choice = '0'
    while choice == '0':
        print("Here is the list of websites to check : \n ")
        for website in monitor.websites:
            print(monitor.websites.index(website) + 1, ' - ', website.URL, '\n')
        print("Would you like to : \n")
        print("\t 1 - Add a website to the list ")
        print("\t 2 - Delete a website from the list")
        print("\t 3 - Run the application")
        choice2 = input("\t\tPlease make a choice: ")

        if choice2 == "1":
            os.system('clear')
            URL = input("Set the website URL: ")
            CheckInterval = int(input("Set The website check interval : "))
            website = Website(URL, CheckInterval)
            monitor.websites.append(website)
        elif choice2 == "2":
            os.system('clear')
            index = input("Enter the index of the website you want to delete from the list: ")
            if (0 < int(index) < len(monitor.websites) + 1):
                monitor.websites.remove(monitor.websites[int(index) - 1])
            else:
                print("\033[93m Wrong index, try again \033[0m")
        elif choice2 == "3":
            # monitor.run_monitor('monitor.db')
            break
            # display = Display(monitor)
            # os.system('clear')
            # run_application(display)



def display_loop(monitor):
    
    update = threading.Timer(10, display_loop,args=[monitor])
    update.start()
    k = displayConsole(10,monitor.hourlyDisplay,monitor)
    monitor.hourlyDisplay += 1
    return k


def main():
    k = 0
    monitor = Monitor()
    menu(monitor)
    monitor.run_monitor('monitor.db')
    print("First display will appear in 10 seconds...")
    time.sleep(10)
    while k != 'q':
        try:
            k = display_loop(monitor)
        except KeyboardInterrupt:
            print("Exiting...")
            break

    menu(monitor)

def main2():
    curses.wrapper(main())


if __name__ == "__main__":
    main2()

        
