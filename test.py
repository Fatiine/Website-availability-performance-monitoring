import requests

from flask import Flask
from threading import Thread
from multiprocessing import Process
from database import create_tables, drop_tables
from monitor import Monitor
from website import Website

# Simple Mock server with Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

def display_test_loop(monitor,n):
    for i in range(5):
        displayConsole(10,monitor.hourlyDisplay,monitor)
        time.sleep(10)

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
    print("Starting the server...")
    server = Process(target=app.run, kwargs={'port':2000})
    server.start()
    stats = monitor.statsPrinter('monitor.db', 10, 1) 
    alerts = monitor.alertsPrinter('monitor.db', 10) 
    monitor.alertsHist = ""
    print(stats)
    print(alerts)

    time.sleep(5)
    stats = monitor.statsPrinter('monitor.db', 10, 1)
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(alerts)

    time.sleep(5)
    stats = monitor.statsPrinter('monitor.db', 10, 1) 
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(alerts)


    #Shut down the server
    print("Shutting down the server ...")
    server.terminate()
    server.join()
    stats = monitor.statsPrinter('monitor.db', 10, 1) 
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(alerts)

    time.sleep(5)
    stats = monitor.statsPrinter('monitor.db', 10, 1) 
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(alerts)

    time.sleep(5)
    stats = monitor.statsPrinter('monitor.db', 10, 1) 
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(alerts)

    # Restart the server
    print("Restarting the server...")
    server = Process(target=app.run, kwargs={'port':2000})
    server.start()
    stats = monitor.statsPrinter('monitor.db', 10, 1) 
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(alerts)

    time.sleep(5)
    stats = monitor.statsPrinter('monitor.db', 10, 1) 
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(alerts)

    time.sleep(5)
    stats = monitor.statsPrinter('monitor.db', 10, 1) 
    alerts = monitor.alertsPrinter('monitor.db', 10)
    monitor.alertsHist = "" 
    print(stats)
    print(alerts)

    print("Shutting down the server ...")
    server.terminate()
    server.join()
