# -*- coding: utf-8 -*-

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
                print("The website : ", self.URL, "is DOWN")
                return False, response

        # Exceptions
        except Exception as e:
            print(' Error !!')
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

    def get_stats(self, timeframe, database_name):
        stats_thread = threading.Timer(10, self.get_stats, args=[timeframe,database_name])
        stats_thread.start()
        # Compute the statistiques of some metrics over a timeframe
        # print("Stats of the website : ", self.URL, "over ", timeframe/60, "minutes ")
        printStr = '\n\033[1;30m ####### Statistiques of the website {} ########\033[0m'.format(self.URL)

        now = datetime.datetime.now()
        time_frame = datetime.timedelta(0, timeframe)
        t = now - time_frame

        selectData = (self.URL, t)

        query_result = select_values(database_name, "monitoring_table", selectData)

        if query_result is None:
            return False, {}

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

        if timeframe == 120:
            if availability < 0.8:
                self.isDown = True
                messageType = "recovery"

                values = (self.URL, time_date, availability, self.isDown, messageType)
                insert_values(database_name, "alerts_table", values)

            if availability >= 0.8 and self.isDown == True:
                self.isDown = False
                messageType = "alert"

                values = (self.URL, time_date, availability, self.isDown, messageType)
                insert_values(database_name, "alerts_table", values)

        values = (self.URL, time_date, timeframe, availability, str(status_code.most_common()), max_RT, min_RT, avg_RT)
        insert_values(database_name, "stats_table", values)

        # print('Availability : ',availability * 100,'%')
        # print('Min response time :', min_RT, 'Max response time :', max_RT, 'Average response time: ', avg_RT)
        # print('Status code:', status_code.most_common())
        printStr += '\n\033[4;36m Past {} minutes:\033[0m'.format(timeframe/60) + \
    '\n\tMax/Avg/Min response time: {:.4f}/{:.4f}/{:.4f} s'.format(max_RT, avg_RT, min_RT) + \
    '\n\tResponse counts: {}'.format(status_code.most_common())+ '\n\tAvailability: {} %'.format(availability*100)
        #print('Availability', availability,  '\n statusCodes': status_code.most_common(), 'maxRT': max_RT, 'minRT:': min_RT, 'avgRT': avg_RT)
        print(printStr)
        return True, {'Availability': availability, 'statusCodes': status_code.most_common(), 'maxRT': max_RT,
                      'minRT:': min_RT, 'avgRT': avg_RT}

    '''def insert_check_data(self, database_name):
        #Inserts the current data into the monitor database
        # Current data
        time_date, availability , status_code , response_time = self.current_data()

        # Database and cursor connection
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()


        sql_command = "INSERT INTO monitoring_table VALUES ( ? , ?, ?, ?, ?)"
        cursor.execute(sql_command, (self.URL, time_date, availability, status_code, response_time))

        # Save the changes before closing
        connection.commit()
        connection.close()
        return'''


    '''def count_stats(self, timeframe, database_name):
        #Compute the statistiques of some metrics over a timeframe 

        # Database and cursor connection
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()

        now = datetime.datetime.now()
        time_frame = datetime.timedelta(0, timeframe) # 2 min
        t = now - time_frame
        
        sql_command = "SELECT * FROM monitoring_table WHERE URL = ? AND timedate >= ?"

        cursor.execute(sql_command,( self.URL, t))
        query_result = cursor.fetchall()
        connection.close()

        if query_result is None:
            return {}
        else:
            availabilities = Counter(element[2] for element in query_result)
            status_code = Counter(element[3] for element in query_result)
            response_times = Counter(element[4] for element in query_result)

            availability = sum(availabilities) / len(availabilities)
            max_RT = max(response_times)
            min_RT = min(response_times)
            avg_RT = sum(response_times) / len(response_times)

        print('Availability : ',availability * 100,'%')
        print('Min response time :', min_RT, 'Max response time :', max_RT, 'Average response time: ', avg_RT)
        print('Status code:', status_code.most_common())
        return'''


    ######################################## Create the website monitor table and intert methods #######################################
    def database_connection(self, database_name):
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        return



    ############################################## End Database methods ##########################################

    #def alerts_check_thread(self, database_name):






        


'''w = Website("http://google.com", 3)
create_tables('test')
w.insert_website_check_thread('test')
w.insert_stats_thread(120,'test')
w.insert_stats_thread(600,'test')'''

