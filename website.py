# -*- coding: utf-8 -*-
import os
import requests
import datetime
import time
import sqlite3
from collections import  Counter
import threading
from database import create_tables, insert_values, select_values



class Website():
    ''' This class has two attributes : 
    - URL of the website
    - checkInterval of the website
    In this class we check the availability of a website 
    and compute the statistiques of its most important metrics '''

    def __init__(self, Url, checkInterval):
        self.URL = Url
        self.checkInterval = checkInterval
        self.isDown = False

    def checkAvailability(self):
        ''' Checks if the URL is alive '''
        try:
            response = requests.get(self.URL)
            status_code = response.status_code
            if status_code in (200, 302):
                #print("The website : ", self.URL, "is UP")
                return True, response
            else :
                #print("The website : ", self.URL, "is DOWN")
                return False, response

        # Exceptions
        except Exception as e:
            #print(' Error !!')
            return False, None

    def current_data(self):
        # Gets the website data at current time
        current_datetime = datetime.datetime.now()  #.strftime("%Y-%m-%d %H:%M:%S")
        availability, response = self.checkAvailability()

        if response is None:
            response_time = status_code = None

        else:
            response_time = response.elapsed.total_seconds()
            status_code = response.status_code

        #print("timedate  :", current_datetime , "availablity: ", availability, "status code: ", status_code, "response time : ", response_time)
        return current_datetime, availability , status_code , response_time

    def insert_website_check(self, database_name):
        continousCheck = threading.Timer(self.checkInterval, self.insert_website_check, args=[database_name])
        continousCheck.start()
        ''' Inserts the current data into the monitor database '''
        # Current data
        time_date, availability , status_code , response_time = self.current_data()
        values = (self.URL, time_date, availability, status_code, response_time)

        insert_values(database_name, "monitoring_table", values)

    def get_stats(self, timeframe, database_name, stats_display_time):
        stats_thread = threading.Timer(stats_display_time, self.get_stats, args=[timeframe,database_name, stats_display_time])
        stats_thread.start()
        os.system('clear')
        # Compute the statistiques of some metrics over a timeframe
        # print("Stats of the website : ", self.URL, "over ", timeframe/60, "minutes ")
        printStr = '\n\033[1;30m ####### Statistiques of the website {} ########\033[0m'.format(self.URL)

        now = datetime.datetime.now()
        time_frame = datetime.timedelta(0, timeframe)
        t = now - time_frame

        selectData = (self.URL, t)

        query_result = select_values(database_name, "monitoring_table", selectData)

        if query_result is None:
            printStr += "No data available"
            return False, {} # "No data available"
            '''False, {}'''

        availabilities = Counter([element[2] for element in query_result if element[2] is not None])
        status_code = Counter([element[3] for element in query_result])
        response_times = [element[4] for element in query_result if element[4] is not None]

        availability = availabilities[True] / sum(availabilities.values())
        max_RT = max(response_times, default=float('inf'))
        min_RT = min(response_times)
        avg_RT = sum(response_times) / len(response_times)
        time_date = datetime.datetime.now()
        # print("availabilities : ", availabilities)
        # print("availabilities[True] :", availabilities[True])
        # print("availability :", availability)

        if timeframe == 120: # 2 minutes
            if availability < 0.8:
                self.isDown = True
                messageType = "alert"

                values = (self.URL, time_date, availability, self.isDown, messageType)
                insert_values(database_name, "alerts_table", values)

            if availability >= 0.8 and self.isDown == True:
                self.isDown = False
                messageType = "recovery"

                values = (self.URL, time_date, availability, self.isDown, messageType)
                insert_values(database_name, "alerts_table", values)

        values = (self.URL, time_date, timeframe, availability, str(status_code.most_common()), max_RT, min_RT, avg_RT)
        insert_values(database_name, "stats_table", values)


        printStr += '\n\033[4;36m Past {} minutes:\033[0m'.format(timeframe/60) + \
    '\n\tMax/Avg/Min response time: {:.4f}/{:.4f}/{:.4f} s'.format(max_RT, avg_RT, min_RT) + \
    '\n\tResponse counts: {}'.format(status_code.most_common())+ '\n\tAvailability: {} %'.format(availability*100)

        print(printStr)
        return True, printStr
        '''{'Availability': availability, 'statusCodes': status_code.most_common(), 'maxRT': max_RT,
                      'minRT:': min_RT, 'avgRT': avg_RT}'''

    def checkAlerts(self, database_name):
        alert_thread = threading.Timer(10 ,self.checkAlerts,args=[database_name])
        alert_thread.start()
        query_result = select_values(database_name, "alerts_table", (self.URL,))

        if query_result is None:
            return False, ''
        else:
            self.alertStr = ""
            for element in query_result:
                if element[4] == 'alert':
                    self.alertStr += '\n\033[4;93m [ALERT MESSAGE !!] \033[0m '+ 'The website {} is DOWN '.format(self.URL) + ' at {}'.format(element[1]+'\t Availability : {} %'.format(element[2]*100))
                elif element[4] == 'recovery':
                    self.alertStr += '\n\033[4;93m [RECOVERY MESSAGE !!] \033[0m '+ 'The website {} is RECOVERED '.format(self.URL) + ' at {}'.format(element[1]+'\t Availability : {} %'.format(element[2]*100))
                print(self.alertStr)
            return True, self.alertStr
