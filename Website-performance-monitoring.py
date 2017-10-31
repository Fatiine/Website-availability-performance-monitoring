import requests
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


def response_time(url):
    response = requests.get(url)
    return response.elapsed.total_seconds()



if __name__ == '__main__':
    print(website_availability("http://google.com/"))
    print(response_time("http://ecodomemaroc.com"))
    print(response_time("http://google.com"))