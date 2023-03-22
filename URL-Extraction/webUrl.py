#importing required packages
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



#url feature extraction 
#1 extracting domain of the url


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


#5  depth of url (sums the number of '/' in url )
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


# 7 checking for https token in domain 
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
    
    
    '''
    
    
    DOMAIN BASED FEATURES EXTRACTION 
    
    
    
    '''
    



#10 dns record availability 
#11 web traffic 

def webTraffic(url):
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

'''

HTML JAVASCRIPT BASED FEATURES


'''


#14 Iframe redirection 
def iframe(response):
    if response =="":
        return 1
    else:
        if re.findall(r"[<iframe>]|<frameBorder>]",response.text):
            return 0
        else:
            return 1
        
        
#15 mouse effect status
def mouseEffect(response):
    if response =="":
        return 1
    else:
        if re.findall("<script>.+onmouseover.+</script>",response.text):
            return 1
        else:
            return 0
        

#16 rightclick attributes checking
def rightClick(response):
    if response =="":
        return 1
    else:
        if re.findall(r"event.button ?=== ?2", response.text):
            return 0
        else:
            return 1
        
# 17 Number of web forwarding
def forwarding(response):
    if response =="":
        return 1
    else:
        if len(response.history) <=2:
            return 0
        else:
            return 1
        
        




def featureExtraction(url):

  features = []
  
  #Address bar based  features (9)
  features.append(ipAddress(url))
  features.append(symbol(url))
  features.append(urlLength(url))
  features.append(depth(url))
  features.append(redirection(url))
  features.append(https(url))
  features.append(is_short_url(url))
  features.append(prefixSuffix(url))
  
 


#  Domain based featurs (4)
  dns = 0
  try:
    domain_name = socket.gethostbyname_ex(url)[-1]
  except:
   dns = 1
  
  features.append(dns)
  features.append(webTraffic(url))
  features.append(1 if dns == 1 else domainAge(domain_name))
  features.append(1 if dns == 1 else domainEnd(domain_name))



    #html and javascript based  features 
  

#   try:
#     response = requests.get(url)
#   except:
#     response = ""
    
#   features.append(iframe(response))
#   features.append(mouseEffect(response))
#   features.append(rightClick(response))
#   features.append(forwarding(response))

  
  return  features



