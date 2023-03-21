#importing required packages
import ssl
from urllib.parse import urlparse,urlencode
import ipaddress 
import re
import requests
import socket
import pandas as pd
import whois
from urllib.parse import urlparse
# from alexapy import Alexa 

import re
import socket
from bs4 import BeautifulSoup
import whois
import urllib
import urllib.request
from datetime import datetime
from selenium import webdriver
import enchant



#url feature extraction 
#1 extracting domain of the url
def domain(url):
    parsed_url = urlparse(url).netloc

    if parsed_url == '':
        return url
    else:
        if re.match(r"www.",parsed_url):
            parsed_url = parsed_url.replace("www.","")
        return parsed_url
    

#2 extracting IP address of url (done)
def ipAddress(url):
    try:
        ip_address = socket.gethostbyname(url)
        return 1
    except:
        return 0


#3 searching for symbol "@" in URL(done)
def symbol(url):
    if "@" in url:
        return 1 
    else:
        return 0


#4  Finding url length (done)
def urlLength(url):
    if len(url) < 54:
        return 0
    else:
        return 1


#5  depth of url (sums the number of '/' in url ) done
def depth(url):
    slash = urlparse(url).path.split ('/')
    depth = 0
    for j in range(len(slash)):
        if len(slash[j]) !=0:
            depth = depth+1
    return depth     


# 6 Number of redirections(done)
def redirection(url):
    num = url.rfind('//')
    if num > 6:
        if num > 7:
            return 1
        else:
            return 0
    else:
        return 0


# 7 checking for https token in domain (done)
def https(url):
    domain = urlparse(url).netloc
    if 'https' in domain:
        return 0
    else:
        return 1
    
    
# 8 Cheking if the url is using shortening services
url_shortening =    r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                    r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                    r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                    r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                    r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                    r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                    r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                    r"tr\.im|link\.zip\.net"
                    
def is_short_url(url):
    match = re.search(url_shortening, url)
    return 1 if match else 0
    
                      
#9 prefix and suffix spereation through (-)in domain (done)
def prefixSuffix(url):
    if '-' in urlparse(url).netloc:
        return 1 #phishing
    else:
        return 0 
    
    

#10 dns record availability
def dnsRecord(url):
    try:
        socket.gethostbyname(url)
        # DNS record is available, URL is more likely to be legitimate
        return 0
    except socket.gaierror:
        # DNS record is not available, URL is more likely to be a phishing attempt
        return 1


#11 web traffic 
def webTraffic(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            # Web traffic is available, URL is more likely to be legitimate
            return 0
        else:
            # Web traffic is not available, URL is more likely to be a phishing attempt
            return 1
    except:
        # Unable to access the URL, URL is more likely to be a phishing attempt
        return 1

        
    
#12 age of damain

def domainAge(domain_name):
    domain_info = whois.whois(domain_name)
    created_date = domain_info.created_date
    expiry_date = domain_info.expiry_date
    if (isinstance(created_date,str) or isinstance(expiry_date,str)):
        try:
            created_date = datetime.strptime(created_date,'%Y-%m-%d')
            expiry_date = datetime.strptime(expiry_date,"%Y-%m-%d")
        except:
            return 1
    if ((expiry_date is None) or (created_date is None)):
        return 1
    elif ((type(expiry_date) is list) or (type(created_date) is list)):
        return 1
    else:
        ageofdomain = abs((expiry_date - created_date).days)
    if ((ageofdomain/30) < 6):
        age = 1
    else:
        age = 0
    return age

# 13 Domain end time 
def domainEnd(domain_name):
    domain_info = whois.whois(domain_name)
    expiration_date = domain_info.expiration_date
    if isinstance(expiration_date,str):
        try:
            expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
        except:
            return 1
    if (expiration_date is None):
        return 1
    elif (type(expiration_date) is list):
        return 1
    else:
        today = datetime.now()
        end = abs((expiration_date - today).days)
        if ((end/30) < 6):
            end = 0
        else:
            end = 1
    return end



#14 Iframe redirection 
def iframe(url):
    try:
        response = requests.get(url).text
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(response, 'html.parser')

        # Find all iFrame elements in the HTML content
        iframes = soup.find_all('iframe')

        if iframes: 
            return 1
        else:
            return 0
    except:
        return 1

        
#15 Use of ssl cerificate
def checkSSL(url):
# send an HTTPS request to the website
    try: 
        response = requests.get(url)

        # check the response headers for the presence of the Strict-Transport-Security header
        if 'Strict-Transport-Security' in response.headers:
            return 0
        else:
            return 1
    except:
        return 1


#16  SSL certificate validity
def sslCheck(url):
  try:
    port = 443
    # Create a socket and wrap it with SSL
    context = ssl.create_default_context()
    with socket.create_connection((url, port)) as sock:
        with context.wrap_socket(sock, server_hostname=url) as sslsock:
            # Get the certificate and its details
            cert = sslsock.getpeercert()
            #   issuer = cert['issuer']
            #   subject = cert['subject']
            #   expiration_date = cert['notAfter']
            # Check if the certificate is valid
            if ssl.match_hostname(cert, url):
                return 0
            else:
                return 1
  except: 
      return 1


#17 Misspelled words in url
def misspell(url):
# retrieve the website content
    try: 
        response = requests.get(url)

        # extract the text content from the HTML
        text = response.text

        # create a dictionary object for the English language
        dictionary = enchant.Dict('en_US')

        # split the text into words and check for misspelled words
        words = text.split()
        misspelled_words = []
        for word in words:
            if not dictionary.check(word):
                misspelled_words.append(word)

        # print the misspelled words
        if len(misspelled_words) > 0:
            return 1
        else:
            return 0
    except: 
        return 1


#18 Presence of pop-up window

def popup(url): 
    try: 
        # set up the Chrome browser
        response = requests.get(url).text
        soup = BeautifulSoup(response, 'html.parser')

        # Check for an element with a class or ID that is associated with a popup
        popup_element = soup.select_one('.popup-class')
        if popup_element:
            return True

        popup_element = soup.select_one('#popup-id')
        if popup_element:
            return 1

        return 0
    
    except:
        return 1

#19 Presence of captcha
def captcha(url):
    try: 
        # send an HTTP request to the website
        response = requests.get(url)

        # parse the response HTML using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # check for the presence of CAPTCHA elements
        if soup.find('input', {'type': 'text', 'name': 'captcha'}) is not None:
            return 0
        else:
            return 1    
    except: 
        return 1



#20 sub domain

def subDomain(url):
    try:
        ip_addresses = socket.gethostbyname_ex(url)[2]

        # loop through the IP addresses and check for subdomains
        subd = []
        for ip_address in ip_addresses:
            reverse_dns = socket.gethostbyaddr(ip_address)[0]
            if reverse_dns != domain:
                subd.append(reverse_dns)

        # print the subdomains, if any
        if len(subd) > 0:
            return 1
        else:
            return 0
        
    except:
        return 1





def featureExtraction(url):

  features = []
  
  
  features.append(domain(url))
  features.append(ipAddress(url))
  features.append(symbol(url))
  features.append(urlLength(url))
  features.append(depth(url))
  features.append(redirection(url))
  features.append(https(url))
  features.append(is_short_url(url))
  features.append(prefixSuffix(url))
  
  
  
  
 
  dns = 0
  try:
    domain_name = socket.gethostbyname_ex(url)[-1]
  except:
   dns = 1
  
  features.append(dns)
  features.append(webTraffic(url))
  features.append(1 if dns == 1 else domainAge(url))
  features.append(1 if dns == 1 else domainEnd(url))

  features.append(iframe(url))
  features.append(checkSSL(domain))
  features.append(sslCheck(domain))
  features.append(misspell(domain))
  features.append(popup(domain))
  features.append(captcha(domain))
  features.append(subDomain(domain))
  

 
  
  return  features




