# -*- coding: utf-8 -*-
import os
import requests
import datetime
import time
import sqlite3
from collections import  Counter
import threading
from database import create_tables, insert_values, select_values
import re



class Website():
    ''' This class has three attributes : 
        - URL (str) : url of the website
        - checkInterval(int): Check Interval of the website
        - isDown (bool): Indicates if the website is down or not
    In this class we check the availability of a website 
    and compute the statistiques of its most important metrics '''

    def __init__(self, Url, checkInterval):
        self.URL = Url
        self.checkInterval = checkInterval
        self.isDown = False

    def normalize_url(self):
        '''adds an http prefix if an url don't have it '''
        if not re.match('^http[s]?://', self.URL):
            self.URL = 'http://' + self.URL
        return self.URL


    def checkAvailability(self):
        ''' Checks if the URL is alive '''
        self.URL = self.normalize_url()
        try:
            response = requests.get(self.URL)
            status_code = response.status_code
            if status_code in (200, 302):
                #print("The website : ", self.URL, "is UP")
                return True, response
            else :
                #print("The website : ", self.URL, "is DOWN")
                self.isDown = True
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
        ''' Inserts the current data into the monitor database '''
        insert_thread = threading.Timer(self.checkInterval, self.insert_website_check, args=[database_name])
        insert_thread.start()
        # Current data
        time_date, availability , status_code , response_time = self.current_data()
        values = (self.URL, time_date, availability, status_code, response_time)

        insert_values(database_name, "monitoring_table", values)

    def get_stats(self, timeframe, database_name):
        ''' Computes the statistiques of some metrics over a defined timeframe '''

        # we calculate the start date we will take into consideration to compute the statistiques
        # The start datetime = actual datetime - timeframe
        now = datetime.datetime.now()
        time_frame = datetime.timedelta(0, timeframe)
        t = now - time_frame

        selectData = (self.URL, t)

        # From our database "database_name", we select the data which is into the timeframe we considered
        select_result = select_values(database_name, "monitoring_table", selectData)

        # it there is no data on the selection result, then we can't compute the statistiques
        if len(select_result) <= 0:
            return False, "\n No available data "

        # if the selection result is not null, we compute the statistiques of the element we select
        availabilities = Counter([element[0] for element in select_result if element[0] is not None])
        status_code = Counter([element[1] for element in select_result])
        response_times = [element[2] for element in select_result if element[2] is not None]

        availability = availabilities[True] / sum(availabilities.values())
        max_RT = max(response_times , default=float('inf'))
        min_RT = min(response_times , default=float('inf'))
        try:
            avg_RT = sum(response_times) / len(response_times)
        except:
            avg_RT = float('inf')
        time_date = datetime.datetime.now()


        # Saves on the table 'alerts_table' on our database if there is a detected alert and when it's recovered
        alertStr =''
        if timeframe == 120: # 2 minutes
            if availability < 0.8 and self.isDown == False:
            # When the availability of a website is < 0.8, then we should save on the data base an alert message
                self.isDown = True
                messageType = "alert"

                values = (self.URL, time_date.strftime("%Y-%m-%d %H:%M:%S"), availability, self.isDown, messageType)
                insert_values(database_name, "alerts_table", values)

                # Saving alert message on "alertStr"
                alertStr = '\n[ALERT MESSAGE !!] '+ 'The website {} is DOWN '.format(self.URL) + ' at {}'.format(time_date.strftime("%Y-%m-%d %H:%M:%S"))+'\t Availability : {:.2f} %'.format(availability*100)

            if availability >= 0.8 and self.isDown == True:
            # Once the availability is >= 0.8, we save on our database a recovery message
                self.isDown = False
                messageType = "recovery"

                values = (self.URL, time_date.strftime("%Y-%m-%d %H:%M:%S"), availability, self.isDown, messageType)
                insert_values(database_name, "alerts_table", values)

                alertStr = '\n[RECOVERY MESSAGE !!] ' + 'The website {} is RECOVERED '.format(self.URL) + ' at {}'.format(time_date.strftime("%Y-%m-%d %H:%M:%S")) + '\t Availability : {:.2f} %'.format(availability * 100)

        


        printStr = '\n Past {} minutes:'.format(timeframe/60) + \
    '\n\tMax/Avg/Min response time: {:.4f}/{:.4f}/{:.4f} s'.format(max_RT, avg_RT, min_RT) + \
    '\n\tResponse counts: {}'.format(status_code.most_common())+ '\n\tAvailability: {:.2f} %'.format(availability*100) + '\n\n' +alertStr

        return True, printStr

    def checkAlerts(self, database_name):
        '''Checks if we have some alert messages on the table "alerts_table" on our database'''

        query_result = select_values(database_name, "alerts_table", (self.URL,))

        # if there is no Alert or Recovery message on the database, we return nothing
        if query_result is None:
            return
        # if there is an Alert or Recovery message on our alerts_table, we add it to the variable self.alertStr where we'll stock all the history of alert messages
        else:
            alertStr = ""
            for element in query_result:
                if element[4] == 'alert':
                    alertStr += '\n[ALERT MESSAGE !!] '+ 'The website {} is DOWN '.format(self.URL) + ' at {}'.format(element[1])+'\t Availability : {:.2f} %'.format(element[2]*100)
                if element[4] == 'recovery':
                    alertStr += '\n[RECOVERY MESSAGE !!] '+ 'The website {} is RECOVERED '.format(self.URL) + ' at {}'.format(element[1])+'\t Availability : {:.2f} %'.format(element[2]*100)
            return alertStr

