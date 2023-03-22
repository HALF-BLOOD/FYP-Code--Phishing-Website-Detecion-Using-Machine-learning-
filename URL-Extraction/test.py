from flask import Flask, request, jsonify
import pickle
import pandas as pd
import webUrl


app = Flask(__name__)

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

    result = {"is_phishing": bool(p), "message": "This website is a phishing website." if p else "This website is not a phishing website."}
    return jsonify(result)

if __name__ == '__main__':
  app.run(debug=True)