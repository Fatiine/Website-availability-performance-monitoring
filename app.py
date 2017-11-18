from website import Website
from monitor import Monitor
from display import Display
import os
import threading
import curses
import time

class Application():
	def __init__(self, monitor):
		self.monitor = monitor

	def menu(self):
	    os.system('clear')
	    choice = '0'
	    while choice == '0':
	        print("\033[95m Welcome to the Website availability & performance monitoring console application \033[0m")
	        print("1 - Enter the website adresses to check and their check intervals")
	        print("2 - Run the test")
	        print("3 - Run the application")

	        choice = input("\t\tPlease make a choice: ")

	        if choice == "1":
	            self.sub_menu1()

	        elif choice == "2":
	            print("Run the test")

	        elif choice == "3":
	        	self.monitor.run_monitor('monitor.db')
	        	self.run_application()
	        else:
	            print("I don't understand your choice.")
	        return

	def sub_menu1(self):
	    os.system('clear')
	    choice = '0'
	    while choice == '0':
	        print("Here is the list of websites to check : \n ")
	        for website in self.monitor.websites:
	            print(self.monitor.websites.index(website) + 1, ' - ', website.URL, '\n')
	        print("Would you like to : \n")
	        print("\t 1 - Add another website ")
	        print("\t 2 - Delete a website from the list")
	        print("\t 3 - Run the application")
	        choice2 = input("\t\tPlease make a choice: ")

	        if choice2 == "1":
	            os.system('clear')
	            URL = input("Set the website URL: ")
	            CheckInterval = int(input("Set The website check interval : "))
	            website = Website(URL, CheckInterval)
	            self.monitor.websites.append(website)
	        elif choice2 == "2":
	            os.system('clear')
	            index = input("Enter the index of the website you want to delete from the list: ")
	            if (0 < int(index) < len(self.monitor.websites) + 1):
	                self.monitor.websites.remove(self.monitor.websites[int(index) - 1])
	            else:
	                print("\033[93m Wrong index, try again \033[0m")
	        elif choice2 == "3":
	        	self.monitor.run_monitor('monitor.db')
	        	self.run_application()

	def main(self):
		console = Display(self.monitor)
		# update_main = threading.Timer(10,console.update_display)
		console.update_display()
		# update_main.start()

	def run_application(self):
		# self.monitor.run_monitor('monitor.db')
		# time.sleep(10)
		curses.wrapper(self.main)


if __name__ == '__main__':
	monitor = Monitor()
	App = Application(monitor)
	App.menu()
	#menu(monitor)