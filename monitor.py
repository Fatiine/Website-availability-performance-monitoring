#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from website import Website
from database import create_tables, drop_tables

class Monitor():
    '''This is the application class
    Attributes : 
        - websites : List of the websites we want to check
        - hourlyDisplay (int) : that attribute indicates when we should display the stats of one hour
                            when it's a multiple of 6 we show the stats of last hour, otherwise we show the stats of last 2 and 10 minutes
        - alertHist (str) : Attribute where we save the history of all alert and recovery messages
        '''
    def __init__(self):
        self.websites = []
        self.hourlyDisplay = 1 # that attribute indicates when we should display the stats of one hour
                            # when it's a multiple of 6 we show the stats of last hour, otherwise we show the stats of last 2 and 10 minutes
        self.alertsHist = ""  # Attribute where we save the history of all alert and recovery messages

    def add_website(self, website):
        '''Function that adds a website to the monitor list of websites'''
        self.websites.append(website)


    def getData(self, database_name):
        ''' Starting the threads to get data of a website and store it in a database'''
        for website in self.websites:
            website.insert_website_check(database_name)

    def statsPrinter(self, database_name, displayInterval, nextHourDisplay):
        ''' Saves on a string statistics that would be sent to the displayer
            Every 10 seconds we send the statistics of the last 2 minutes and the last 10 minutes
            And every 1 minutes we send the statistics of the last hour  
            So we send 5 times the stats of 2 and 10 minutes, and on the sixth time we send the stats of one hour '''
        
        if nextHourDisplay%6 == 0:
            hourDisplay = True
        else:
            hourDisplay = False

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
            if not (stats2m_bool and stats10m_bool and (not hourDisplay or stats60m_bool)):
                printStr += "\nNo data available !! "

        return printStr

    def alertsPrinter(self, database_name, displayTime):
        ''' Saves on the attribute "self.alertsHist" all the history of alert and recovery messages of all the websites on the monitor list '''
        for website in self.websites:
            self.alertsHist += website.checkAlerts(database_name)
        return self.alertsHist


    def run_monitor(self, database_name):
        '''Drops the tables of the database "database_name" and creates new tables
        Starts saving data of each website of the monitor websites list over their appropriate checkInterval'''
        drop_tables('monitor.db')
        create_tables('monitor.db')
        self.getData('monitor.db')
