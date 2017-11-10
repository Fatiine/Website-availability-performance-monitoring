# -*- coding: utf-8 -*-

import requests
import datetime
import time



class Website():
 
    def __init__(self, Url, checkInterval):
        self.URL = Url
        self.checkInterval = checkInterval
        #self.alerts = Alert()

    def checkAvailability(self):
        # First check internet connection
        # if not (self.internet_on()):
        #     print("There is no internet connection !")
        #     return
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
        # Get the website data at current moment 
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        availablity, response = self.checkAvailability()

        if response is None:
            response_time = status_code = None

        else:
            response_time = response.elapsed.total_seconds()
            status_code = response.status_code

        print("timedate  :", now , "availablity: ", availablity, "status code: ", status_code, "response time : ", response_time)
        return
