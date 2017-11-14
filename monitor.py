#!/usr/bin/env python3

from website import Website
from database import create_tables
import threading
import os
import datetime

class Monitor():
    '''This is the application class
    Attributes : 
        - List of the websites we want to check
        - Console 
        '''

    def __init__(self):
        self.websites = []

    def add_website(self, website):
        '''Function that adds a website to the monitor list of websites'''
        w = Website(website[0], website[1])
        self.websites.append(w)



    def menu(self):
        choice = '0'
        while choice == '0':
            print("Main Choice: Choose 1 of 3 choices")
            print("1 - Enter the website adresses to check and their check intervals")
            print("2 - Run the test")
            print("3 - Run the application")

            choice = input("Please make a choice: ")

            if choice == "1":
                self.sub_menu1()

            elif choice == "2":
                print("Do Something 2")
            elif choice == "3":
                self.run_application()
            else:
                print("I don't understand your choice.")
            return

    def sub_menu1(self):
        choice = '0'
        while choice == '0':
            print("Here is the list of websites to check : \n ")
            for website in self.websites:
                print(self.websites.index(website) + 1, ' - ', website.URL, '\n')
            print("Would you like to : \n")
            print("1 - Add another website ")
            print("2 - Delete a website")
            print("3 - Go back to the menu")
            choice2 = input("Please make a choice: ")

            if choice2 == "1":
                URL = input("Set the website URL: ")
                CheckInterval = int(input("Set The website check interval : "))
                website = Website(URL, CheckInterval)
                self.websites.append(website)
            elif choice2 == "2":
                index = input("Enter the index of the website you want to delete : ")
                if (0 < int(index) < len(self.websites) + 1):
                    self.websites.remove(self.websites[int(index) - 1])
                else:
                    print("Wrong index, try again")
            elif choice2 == "3":
                self.menu()

    def getData(self, database_name):
        # Starting a thread to get data of a website and store it in a database
        for website in self.websites:
            #continuous_Check = threading.Timer(website.checkInterval, website.insert_website_check_thread, args=[database_name])
            #continuous_Check.start()
            website.insert_website_check(database_name)


    def getStats(self,timeframe, database_name, displayTime):
        # Starting a thread to get the statististiques of each website in the database
        for website in self.websites:
            continuousStats = threading.Timer(displayTime, website.get_stats, args=[timeframe, database_name])
            continuousStats.start()


    def run_monitor(self, database_name):

        self.getData(database_name)


        self.getStats(120, database_name, 10)
        self.getStats(600,database_name, 10)
        self.getStats(600, database_name, 60)



m = Monitor()
w = ("http://yahoo.fr", 5)
w2 = ("http://enpc.fr/", 3)
w3 = ("http://ecodomemaroc.com/", 4)

m.add_website(w)
m.add_website(w2)
m.add_website(w3)

create_tables('monitor')
m.run_monitor('monitor')
