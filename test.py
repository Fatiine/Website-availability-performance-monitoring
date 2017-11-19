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
    return 'Hello, World!'

def test_alert_logic():
    os.system('clear')
    ''' tests the alerting logic using a mock server '''

    #remove flask's logs
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    # Create monitor 
    monitor = Monitor()
    # Local url 
    url = 'http://localhost:2000'
    checkInterval = 2
    # Creating object website
    website = Website(url,checkInterval)

    #Attach website to monitor
    monitor.add_website(website)

    # drop the tables in the test database and create new ones
    drop_tables('test.db')
    create_tables('test.db')

    # run monitor 
    monitor.run_monitor('test.db')

    # Start server 
    print(colored("Starting the server...",'green'))
    server = Process(target=app.run, kwargs={'port':2000})
    server.start()

    time.sleep(1)

    stats = monitor.statsPrinter('monitor.db', 10, 1) 
    alerts = monitor.alertsPrinter('monitor.db', 10) 
    monitor.alertsHist = ""
    print(stats)
    print(colored(alerts,'red'))

    time.sleep(10)
    stats = monitor.statsPrinter('monitor.db', 10, 1)
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(colored(alerts,'red'))

    time.sleep(10)
    stats = monitor.statsPrinter('monitor.db', 10, 1)
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(colored(alerts,'red'))

    time.sleep(10)
    stats = monitor.statsPrinter('monitor.db', 10, 1)
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(colored(alerts,'red'))

    time.sleep(10)
    stats = monitor.statsPrinter('monitor.db', 10, 1)
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(colored(alerts,'red'))




    #Shut down the server
    print(colored("Shutting down the server ...",'yellow'))
    server.terminate()
    server.join()
    stats = monitor.statsPrinter('monitor.db', 10, 1) 
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(colored(alerts,'red'))

    time.sleep(10)
    stats = monitor.statsPrinter('monitor.db', 10, 1) 
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(colored(alerts,'red'))

    

    # Restart the server
    print(colored("Re-starting the server...",'green'))
    server = Process(target=app.run, kwargs={'port':2000})
    server.start()
 
    stats = monitor.statsPrinter('monitor.db', 10, 1) 
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(colored(alerts,'red'))

    time.sleep(10)
    stats = monitor.statsPrinter('monitor.db', 10, 1) 
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(colored(alerts,'red'))

    time.sleep(10)
    stats = monitor.statsPrinter('monitor.db', 10, 1) 
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(colored(alerts,'red'))

    time.sleep(10)
    stats = monitor.statsPrinter('monitor.db', 10, 1) 
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(colored(alerts,'red'))

    time.sleep(10)
    stats = monitor.statsPrinter('monitor.db', 10, 1) 
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(colored(alerts,'red'))

    time.sleep(10)
    stats = monitor.statsPrinter('monitor.db', 10, 1) 
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(colored(alerts,'red'))

    print(colored("Shutting down the server ...",'yellow'))
    server.terminate()
    server.join()
