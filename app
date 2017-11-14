
Launch the monitor and store the data on a database with the appropriate data datetime

# Stats : 
- Every CheckInterval calculate the statistiques of the data we have on the database over 2 min and 10 min
- Every 10s, display the stats of the past 10min 
- Every 1min, display the stats of the past 1 hour

#Alert 


Classes : 

- Website : 
        Attributes : 
            - URL : the url of the website ( user defined )
            - checkInterval : the frequency of the website check ( user defined )

        Methods :
            - checkAvailability : Checks if the URL is Alive and return a boolean (True: is Alive, False : isn't alive ) and the response of the GET request we send
            - current_data : Gets the website data ( availability , response time and status code ) at the current time, and returns those data 
            - insert_website_check(database_name): Inserts the current data into the monitor database 
            - get_stats(timeframe, database_name) : Gets the statistiques of the website over the timeframe defined


- Monitor : 
        Attributes : 
            - websites : List of the websites we want to check their availabilities and performances 
            - console : 
        
        Methods : 
            - getData(database_name) : Saves on the database " database_name " the metrics of each website on the websites list in their check intervals.
            - display_stats(displayTime, database_name, stats_column) : Displays the statistiques of each 
