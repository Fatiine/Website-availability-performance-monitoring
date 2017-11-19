# Website-availability-performance-monitoring

## About the console program 
This console program allows the user to monitor the performance and the availability of a website.
It started with a simple menu that asks the user to enter the websites he wants to monitor and the appropriate check intervals. 
There is a possibility to delete or add a website on the list of websites the monitor checks.
The results appear in two columns, one dedicated for statistics, and the other for alerts.
When the user is asked to enter the website's url, we check if that URL verify the http url format. If not we ask them to try again. We do the same thing with the check Interval.
When we start to run the program, a sqlite database is created. We store on a table called "monitoring_table" the metrics of each website in their appropriate check Intervals.
We store also on a table called "alerts_table" the alert and recovery messages. The user can open this database to see the history of alert messages.


The console program created is composed of 2 key classes :
- Website ( website.py ): 
    Attributes : 
        - URL (url) : the url of the website ( user defined )
        - checkInterval (int) : the frequency of the website check ( user defined )
        - isDown(bool): Indicates if the website is alive or not

    Methods :
        - normalize_url() : Which adds an http prefix if a user define an url without it
        - checkAvailability() : Checks if the URL is Alive and return a boolean (True: is Alive, False : isn't alive ) and the response of the GET request we send
        - current_data() : Gets the website data ( availability , response time and status code ) at the current time, and returns those data 
        - insert_website_check(database_name): Inserts the current data into the monitor database 
        - get_stats(timeframe, database_name) : Gets the statistiques of the website over the timeframe defined
        - checkAlerts(database_name) : Checks if we have some alert messages on the table "alerts_table" on our database
- Monitor (monitor.py) : 
    Attributes : 
        - websites : List of the websites we want to check their availabilities and performances 
        - hourlyDisplay (int) : that attribute indicates when we should display the stats of one hour. When it's a multiple of 6 we show the stats of last hour, otherwise we show the stats of last 2 and 10 minutes.
    - alertHist (str) : Attribute where we save the history of all alert and recovery messages 
    
    Methods : 
        - add_website(website): Function that adds a website to the monitor list of websites
        - getData(database_name) : Saves on the database " database_name " the metrics of each website on the websites list in their check intervals.
        - statsPrinter(database_name, displayInterval, nextHourDisplay): Saves on a string statistics that would be sent to the displayer
            Every 10 seconds we send the statistics of the last 2 minutes and the last 10 minutes
            And every 1 minutes we send the statistics of the last hour  
            So we send 5 times the stats of 2 and 10 minutes, and on the sixth time we send the stats of one hour
        - alertsPrinter(database_name, displayTime) : Saves on the attribute "self.alertsHist" all the history of alert and recovery messages of all the websites on the monitor list 
        - run_monitor(database_name): Drops the tables of the database "database_name" and creates new tables.
        Starts saving data of each website of the monitor websites list over their appropriate checkInterval.

and :
- database.py : 
        This file contains all the functions that allow us create a table on a sqlite database, insert values into a table and select values from a table.

- main.py : 
        File where the menu and display functions are defined.

## Usage : 
On a terminal, run the command : 
        python3 main.py 
Then follow the instructions.


## Requirements:
To run this program, you need to have python3 and pip3.
Then you need to install the libraries or modules :( curses, threading, sqlite3, requests, datetime, time, sys, os, re , logging, multiprocessing, flask) using the command : 
>> sudo pip install [module_name]


## Test:
For the test, I created a mock-server (local server ) that responds to GET requests. I started the server, then I shut it down and re-start it again to test the alert logic.


## How the application can be improved : 
- Verify if the URL the user has defined exists, which means if it has an existing DNS adress. 
- Implementation of Background workers or Asynchronous tasks that can compute the stats asynchronouly. This will make sure that the calculation are done the moment they are needed to be done without any delays.
- Add some statistical calculations that will help in the troubleshooting process of a low availability website for example and will alert of a risk of a statistical high chance of a website going down during a period of time.
- Instead of using several timeframes(2, 10 and 60 minutes), we can make a UI that displays a graph stating the in-real-time variations of the stats;
Each check interval, the graph will be updated with puntual values + the moving averages of the availabilty, response time and other interesting stats.All the website can be stacked into one graph that can make the reading much easier.
- The application is about monitoring, so adding some sound alarms might be an ergonomic bonus.


