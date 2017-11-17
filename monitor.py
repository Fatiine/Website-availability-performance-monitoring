#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from website import Website
from database import create_tables
import threading
import curses
import os
import datetime
import sys
import select

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
        self.websites.append(website)

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
            website.insert_website_check(database_name)


    # def getStats(self, database_name, displayTime):
    #     Stats = threading.Timer(displayTime, self.getStats, args=[database_name, displayTime])
    #     Stats.start()
    #     for website in self.websites:
    #         printStr = '\n\033[4;93m ####### Statistiques of the website {} ########\033[0m'.format(website.URL)
    #         website.get_stats(120,database_name,printStr)
    #         website.get_stats(600,database_name, printStr)
    # def getStats(self,timeframe, database_name, displayTime):
    #     for website in self.websites:
    #         Stats = threading.Timer(displayTime, website.get_stats, args=[timeframe, database_name, displayTime])
    #         Stats.start()
        
    def getStats(self,database_name,displayTime):
        # os.system('clear')
        if displayTime == 10:
            for website in self.websites:
                printStr = '\n\n ######### Statistiques of the website {} #########\033[0m'.format(website.URL)
                printStr2 = website.get_stats(120,database_name, displayTime, printStr)
                website.get_stats(600,database_name, displayTime, printStr2)
        if displayTime == 60:
            for website in self.websites:
                printStr = '\n\n ######### Statistiques of the website {} #########\n\n'.format(website.URL)
                website.get_stats(3600,database_name, displayTime, printStr)
        return printStr

    def statsPrinter(self, database_name, displayInterval, nextHourDisplay):
        if nextHourDisplay == 0:
            stats = threading.Timer(displayInterval, self.statsPrinter, args=[database_name, displayInterval, 5])
            hourDisplay = True
        else:
            stats = threading.Timer(displayInterval, self.statsPrinter,
                                    args=[database_name, displayInterval, nextHourDisplay - 1])
            hourDisplay = False
        stats.start()

        printStr = ""
        for website in self.websites:
            printStr += '\n\n ######### Statistiques of the website {} #########'.format(website.URL)
            stats2m_bool, stats2m_data = website.get_stats(120, database_name)  #  Statistiques of past 2 minutes
            stats10m_bool, stats10m_data = website.get_stats(600, database_name)  #  Statistiques of past 10 minutes
            stats60m_bool, stats60m_data = website.get_stats(3600, database_name)  #  Statistiques of past hour
            alerts = website.checkAlerts(database_name)
            if stats2m_bool and not (hourDisplay):
                printStr += stats2m_data
            if stats10m_bool and not (hourDisplay):
                printStr += stats10m_data
            if stats60m_bool and hourDisplay:
                printStr += stats60m_data
            if not (stats2m_bool and stats10m_bool and not (stats60m_bool or stats60m_bool)):
                printStr += "No data available"

        return printStr

    def getStatsPrinter(self, database_name, displayInterval, nextHourDisplay):
        stats = threading.Timer(10, self.statsPrinter, args=[database_name, displayInterval, nextHourDisplay])
        stats.start()

    def alertsPrinter(self, database_name, displayTime):
        self.alertsHist = ""
        #alerts = threading.Timer(10, self.alertsPrinter, args=[database_name, displayTime])
        #alerts.start()
        for website in self.websites:
            self.alertsHist += website.checkAlerts(database_name)
        return self.alertsHist

    def getStatsThread(self,displayTime, database_name):
        statsRes = threading.Timer(displayTime,self.getStats, args=[database_name,displayTime])
        statsRes.start()

    def getAlerts(self,database_name):
        for website in self.websites:
            Alerts = threading.Timer(10, website.checkAlerts, args=[database_name])
            Alerts.start()

    def run_monitor(self, database_name):
        # TO DO: drop tables on the database 'monitor.db' before starting to write data on it
        # Begins by creating a database with 2 tables, monitoring_table and alerts_table
        create_tables('monitor.db')
        self.getData('monitor.db')







# m = Monitor()
# w = Website("http://yahoo.fr", 2)
# w2 = Website("http://enpc.fr/", 3)
# w3 = Website("http://ecodomemroc.com/", 4)

# m.add_website(w)
# m.add_website(w2)

# create_tables('monitor.db')
# m.getData('monitor.db')
# m.run_monitor('monitor.db')



