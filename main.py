import sys, os
import curses
from website import Website
from monitor import Monitor
from database import create_tables
import time
import threading
import re 
from test import test_alert_logic



def displayConsole(displayTime,hourlyCheck, monitor):
    ''' Displays in two columns : 'Statistiques ' and 'Alerts' the updated data every displatTime '''

    line = monitor.statsPrinter('monitor.db', displayTime, hourlyCheck) # Data we'll display on the column "Statistiques"
    line2 = monitor.alertsPrinter('monitor.db', displayTime) # Data we'll display on the column "Alerts"
    monitor.alertsHist = "" 

    monitor.hourlyDisplay += 1
    k = 0

    # Clear and refresh the screen
    myscreen = curses.initscr()
    myscreen.clear()
    myscreen.refresh()

    # Initialize colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    # curses.curs_set(0)

    while (k != ord('q')):
        '''Draw borders of the different columns'''
        height, width = myscreen.getmaxyx()
        myscreen.border()
        myscreen.refresh()

        '''Initialize the Statistics column'''
        stats_column = curses.newwin(height - 2, width // 2, 1,
                                     1)
        _, a_x = stats_column.getmaxyx()
        stats_column.scrollok(True)
        stats_column.setscrreg(3,height - 3)
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
        stats_column.setscrreg(3,height - 3)
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

        # Render status bar
        statusbarstr = "Press 'q' to exit  "
        myscreen.attron(curses.color_pair(3))
        myscreen.addstr(height - 1, 0, statusbarstr)
        myscreen.addstr(height - 1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        myscreen.attroff(curses.color_pair(3))

        # Turning on attributes for title
        myscreen.attron(curses.color_pair(2))
        myscreen.attron(curses.A_BOLD)

        # Turning off attributes for title
        myscreen.attroff(curses.color_pair(2))
        myscreen.attroff(curses.A_BOLD)

        myscreen.move(height - 2, width - 2)

        # Refresh the screen
        myscreen.refresh()

        k = myscreen.getch()

        if( k == ord('q')):
            curses.endwin()
            os._exit(0)


def normalize_url(url):
    '''adds an http prefix if an url don't have it '''
    if not re.match('^http[s]?://', url):
        url = 'http://' + url
    return url     

def is_http_url(s):
    '''Returns true if s is valid http url, else false '''
    if re.match('https?://(?:www)?(?:[\w-]{2,255}(?:\.\w{2,6}){1,2})(?:/[\w&%?#-]{1,300})?',s):
        return True
    else:
        return False   

def menu(monitor):
    ''' Asks the user to define the website URL and CheckInterval  '''
    choice = '0'
    while choice == '0':
        print("\033[95m Welcome to the Website availability & performance monitoring console application \033[0m")
        print("1 - Enter the website adresses to check and their check intervals")
        print("2 - Run the test")
        print("3 - Exit")

        choice = input("\t\tPlease make a choice: ")

        if choice == "1":
            sub_menu1(monitor)

        elif choice == "2":
            print("Run the test")
            test_alert_logic()

        elif choice == "3":
            os._exit(0)

        else:
            print("I don't understand your choice.")
            menu(monitor)

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

            # If the user define a non existant URL or a wrong value on the checkInterval we ask them to try again 
            while True:
                try:
                    URL = input("Set the website URL \n (format examples : google.fr or http://google.fr) : ")
                    URL = normalize_url(URL)
                    if( is_http_url(URL) ):
                        break
                    else:
                        print("\033[31m Sorry, This is not a valid http url, Try again :) \033[0m")
                        continue
                except:
                    print("\033[31m Sorry, This is not a valid http url, Try again :) \033[0m")
                    continue

            
            while True:
                try:
                    CheckInterval = float(input("Set The website check interval (in seconds) : "))
                except ValueError:
                    print("That's not an int!")
                    continue
                else:
                    break
     
            website = Website(URL, CheckInterval)
            monitor.websites.append(website)

        elif choice2 == "2":
            os.system('clear')
            index = input("Enter the index of the website you want to delete from the list: ")
            if (0 < int(index) < len(monitor.websites) + 1):
                monitor.websites.remove(monitor.websites[int(index) - 1])
            else:
                print("\033[31m Wrong index, try again \033[0m")

        elif choice2 == "3":
            break


def display_loop(monitor):
    '''Updates the display every 10 seconds'''
    update_display = threading.Timer(10, display_loop,args=[monitor])
    update_display.start()
    displayConsole(10,monitor.hourlyDisplay,monitor)

def main():
    ''' Main function '''
    monitor = Monitor()
    menu(monitor)
    if len(monitor.websites) > 0 :
        monitor.run_monitor('monitor.db')
        print("First statistics will appear in 10 seconds...")
        time.sleep(10)
        monitor.hourlyDisplay = 1
        display_loop(monitor)
    else:
        print('\033[93m The websites list is empty !! Please define the websites you want to monitor their performances \033[0m')
        main()

def run_application():
    curses.wrapper(main())


if __name__ == "__main__":
    run_application()
