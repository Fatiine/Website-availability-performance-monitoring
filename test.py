import requests
import os
import time
from flask import Flask
from threading import Thread
from multiprocessing import Process
import logging
from database import create_tables, drop_tables
from monitor import Monitor
from website import Website
from termcolor import colored
# Simple Mock server with Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World! \n I\'m a test server '

def test_alert_logic():
    os.system('clear')
    ''' tests the alerting logic using a mock server '''

    # remove flask's logs
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    print(colored("The idea is to create a mock server at \"http://localhost:2000\" and test the alert system",'yellow'))
    
    print("Creating the monitor...  \n adding \"http://localhost:2000\" and a check interval (2 seconds ) to its websites list... ")

    # Create monitor 
    monitor = Monitor()
    # Local url 
    url = 'http://localhost:2000'
    checkInterval = 2
    # Creating object website
    website = Website(url,checkInterval)

    #Attach website to monitor
    monitor.add_website(website)

    print("Running the monitor before starting the server... ")
    # run monitor 
    monitor.run_monitor('test.db')

    print("Computing first stats, and checking if there are any alerts ... ")

    stats = monitor.statsPrinter('monitor.db', 10, 1) 
    alerts = monitor.alertsPrinter('monitor.db', 10) 
    monitor.alertsHist = ""
    print(stats)
    print(colored(alerts,'red'))

    print(colored("As expected, As the server is already DOWN, the program sends an alert message ! ",'yellow'))


    # Start server 
    print(colored("Starting the server...",'green'))
    server = Process(target=app.run, kwargs={'port':2000})
    server.start()

    print("Computing stats every 10 seconds, and checking if there are any alerts messages ... ")
    print("First calculations ...")
    time.sleep(10)
    stats = monitor.statsPrinter('monitor.db', 10, 1)
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(colored(alerts,'red'))

    print("Second calculations ...")
    time.sleep(10)
    stats = monitor.statsPrinter('monitor.db', 10, 1)
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(colored(alerts,'red'))

    print("Third calculations ...")
    time.sleep(10)
    stats = monitor.statsPrinter('monitor.db', 10, 1)
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(colored(alerts,'red'))

    print("Fourth calculations ...")
    time.sleep(10)
    stats = monitor.statsPrinter('monitor.db', 10, 1)
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(colored(alerts,'red'))

    print(colored("When the server starts, and the availability becomes >= 0.8, the alerting system sends a recovery message. At the same time it prints also the previous alert messages ",'yellow'))


    #Shut down the server
    print(colored("Shutting down the server again...",'green'))
    server.terminate()
    server.join()
    time.sleep(1)
    print("Computing stats after 1 second, and checking if there are any alerts or recovery messages ... ")
    stats = monitor.statsPrinter('monitor.db', 10, 1) 
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(colored(alerts,'red'))

    print("Computing stats after 10 seconds, and checking if there are any alerts or recovery messages ... ")
    time.sleep(10)
    stats = monitor.statsPrinter('monitor.db', 10, 1) 
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(colored(alerts,'red'))

    print(colored("It the availability becomes < 0.8, the alerting system sends an alert message. \n It prints also the previous alert and recovery messages ",'yellow'))

    # Restart the server
    print(colored("Re-starting the server...",'green'))
    server = Process(target=app.run, kwargs={'port':2000})
    server.start()
    time.sleep(1)

    print("Computing stats after 1 second, and checking if there are any alerts or recovery messages ... ") 
    stats = monitor.statsPrinter('monitor.db', 10, 1) 
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(colored(alerts,'red'))

    print("Computing stats after 10 seconds, and checking if there are any alerts or recovery messages ... ") 
    time.sleep(10)
    stats = monitor.statsPrinter('monitor.db', 10, 1) 
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(colored(alerts,'red'))

    print("Computing stats after 10 seconds, and checking if there are any alerts or recovery messages ... ") 
    time.sleep(10)
    stats = monitor.statsPrinter('monitor.db', 10, 1) 
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(colored(alerts,'red'))

    print("Computing stats after 10 seconds, and checking if there are any alerts or recovery messages ... ") 
    time.sleep(10)
    stats = monitor.statsPrinter('monitor.db', 10, 1) 
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(colored(alerts,'red'))

    print("Computing stats after 10 seconds, and checking if there are any alerts or recovery messages ... ") 
    time.sleep(10)
    stats = monitor.statsPrinter('monitor.db', 10, 1) 
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(colored(alerts,'red'))

    print("Computing stats after 10 seconds, and checking if there are any alerts or recovery messages ... ") 
    time.sleep(10)
    stats = monitor.statsPrinter('monitor.db', 10, 1) 
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(colored(alerts,'red'))

    print(colored("It the availability becomes >= 0.8, the alerting system sends a recovery message. \n It keeps always the previous alert and recovery messages (For historical reasons ;) ",'yellow'))

    print(colored("Shutting down the server ...",'yellow'))
    server.terminate()
    server.join()

    print(colored("A database \"test.db\" is created and it saves all the ALERT and RECOVERY messages"))
    print(colored("End of the test",'blue'))