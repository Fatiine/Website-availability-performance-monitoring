import requests
import time
from http.client import HTTPConnection
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen



def website_availability(url):
    try:
        open_url = urlopen(url)
        status_code = open_url.getcode()
        if status_code  == 200:
            return 'UP', open_url
    except:
        pass
    return 'DOWN', open_url

def store_response_times(url, timeframe):
    resp_time = []
    t = time.time()
    #print(t+timeframe)
    while(time.time() < t+timeframe):
        #print(time.time())
        resp_time.append(response_time(url))
    return resp_time


def response_time(url):
    # should define a timeout
    response = requests.get(url)
    return response.elapsed.total_seconds()


def response_time_stats(response_time):
    print("Max response time : " , max(response_time))
    print("Min response time : " , min(response_time))
    print("Avr response time : " , sum(response_time)/len(response_time))
    return


if __name__ == '__main__':
    print(website_availability("http://google.com/"))
    print(response_time("http://yahoo.fr"))
    print(response_time("http://google.com"))
    print(response_time_stats(store_response_times("http://google.com",0.5)))
    print(response_time_stats(store_response_times("http://yahoo.fr", 0.5)))