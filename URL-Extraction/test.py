import pickle
import pandas as pd
import webUrl


data=[]
data.append(webUrl.featureExtraction("https://www.mail.beloinox.pl"))

feature_names = ['Have_IP', 'Have_At', 'URL_Length', 'URL_Depth','Redirection', 
                      'https_Domain', 'TinyURL', 'Prefix/suffix', 'DNS_Record', 'Web_Traffic', 
                      'Domain_Age', 'Domain_End']
data2 = pd.DataFrame(data, columns= feature_names)

model = pickle.load(open("XGBoostClassifier.pickle.dat", "rb"))
p = model.predict(data2)
print (p)