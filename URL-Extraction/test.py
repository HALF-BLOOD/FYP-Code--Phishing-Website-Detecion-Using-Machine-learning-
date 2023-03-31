from flask import Flask, request, jsonify
import pickle
import pandas as pd
import webUrl
import os
import ctypes
import sys
from urllib.parse import urlparse, urlsplit
from flask import Flask, request, jsonify, send_from_directory
import re

app = Flask(__name__)



def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit(0)


@app.route('/check-phishing', methods=['POST', 'OPTIONS'])
def check_phishing():
    if request.method == 'OPTIONS':
        # Set CORS headers
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        return ('', 204, headers)

    url = request.json['url']
    print(f'Received URL: {url}')
    
    data=[]
    data.append(webUrl.featureExtraction(url))

    feature_names = ['Have_IP', 'Have_At', 'URL_Length', 'URL_Depth','Redirection', 
                          'https_Domain', 'TinyURL', 'Prefix/suffix', 'DNS_Record', 'Web_Traffic', 
                          'Domain_Age', 'Domain_End']
    data2 = pd.DataFrame(data, columns= feature_names)

    model = pickle.load(open("XGBoostClassifier.pickle.dat", "rb"))
    p = model.predict(data2)
    print (p)

    if p:
        add_to_hosts_file(url)

    result = {"is_phishing": bool(p), "message": "This website is a phishing website." if p else "This website is not a phishing website."}
    return jsonify(result)



def add_to_hosts_file(url):
    hosts_path = os.path.join('C:', os.sep, 'Windows', 'System32', 'drivers', 'etc', 'hosts')
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    
    try:
        with open(hosts_path, 'a') as hosts_file:
            hosts_file.write(f'127.0.0.1 {hostname}\n')
            print(f'Added {hostname} to hosts file.')
    except Exception as e:
        print(f'Error adding {hostname} to hosts file: {e}')



@app.route('/')
def blocked_page():
    return send_from_directory('.', 'blocked.html')



# __________________________Remove from hosts file_______________________________
@app.route('/remove-from-hosts', methods=['POST', 'OPTIONS'])
def remove_from_hosts():
    if request.method == 'OPTIONS':
        # Set CORS headers
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        return ('', 204, headers)

    url = request.json['url']
    print(f'Removing URL: {url}')
    remove_from_hosts_file(url)
    return jsonify({"message": f"{url} has been removed from the hosts file."})

def remove_from_hosts_file(url):
    hosts_path = os.path.join('C:', os.sep, 'Windows', 'System32', 'drivers', 'etc', 'hosts')
    match = re.search(r'(.*)', url)
    hostname = match.group(1) if match else None
    print(f'Parsed hostname: {hostname}')
    lines = []

    try:
        with open(hosts_path, 'r') as hosts_file:
            lines = hosts_file.readlines()

        with open(hosts_path, 'w') as hosts_file:
            for line in lines:
                if line.strip() == f'127.0.0.1 {hostname}':
                    continue
                else:
                    hosts_file.write(line)

        print(f'Removed {hostname} from hosts file.')
    except Exception as e:
        print(f'Error removing {hostname} from hosts file: {e}')




@app.route('/blocked-urls', methods=['GET', 'OPTIONS'])
def blocked_urls():
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        return ('', 204, headers)

    hosts_path = os.path.join('C:', os.sep, 'Windows', 'System32', 'drivers', 'etc', 'hosts')
    blocked_urls = []

    with open(hosts_path, 'r') as hosts_file:
        for line in hosts_file:
            match = re.search(r'127\.0\.0\.1\s+(\S+)', line)
            if match:
                blocked_urls.append(match.group(1))

    return jsonify(blocked_urls)





if __name__ == '__main__':
  app.run(debug=True)
