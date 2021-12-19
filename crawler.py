#!/usr/local/bin/python3


#importing libraries
from IPython.display import Image
from IPython.core.display import HTML
#import os
import csv

from termcolor import colored, cprint

import datetime
import json
import urllib.request

import json 
import pandas as pd 
from pandas.io.json import json_normalize #package for flattening json in pandas df

import time


####################################

def url_builder(city_id,city_name,country):
    user_api = 'f2573f2c32c60b5915dbcaba22fbbbb8'  # chaged to personnal key, Obtain yours form: http://openweathermap.org/
    unit = 'metric'  # For Fahrenheit use imperial, for Celsius use metric, and the default is Kelvin.
    if(city_name!=""):
        api = 'http://api.openweathermap.org/data/2.5/weather?q=' # "http://api.openweathermap.org/data/2.5/weather?q=Tunis,fr
        full_api_url = api + str(city_name) +','+ str(country)+ '&mode=json&units=' + unit + '&APPID=' + user_api
    else:
        api = 'http://api.openweathermap.org/data/2.5/weather?id='     # Search for your city ID here: http://bulk.openweathermap.org/sample/city.list.json.gz
        full_api_url = api + str(city_id) + '&mode=json&units=' + unit + '&APPID=' + user_api
   
    return full_api_url


#################################################

def data_fetch(full_api_url):
    url = urllib.request.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    raw_api_dict = json.loads(output)
    url.close()
    return raw_api_dict


#full_api_url=url_builder(city_id,'','')
#data=data_fetch(full_api_url)
#print(colored(data, 'yellow',attrs=['bold']))


##################################################################

def time_converter(time):
    converted_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%I:%M %p')
    return converted_time

###################################################################

def data_organizer(raw_api_dict):
    data = dict(
        city=raw_api_dict.get('name'),
        country=raw_api_dict.get('sys').get('country'),
        temp=raw_api_dict.get('main').get('temp'),
        temp_max=raw_api_dict.get('main').get('temp_max'),
        temp_min=raw_api_dict.get('main').get('temp_min'),
    )
    print (data)
    return data

#######################################################################

def data_output(data):
    m_symbol = '\xb0' + 'C'
    print('---------------------------------------')
    print('Current weather in: {}, {}:'.format(data['city'], data['country']))
    print(data['temp'], m_symbol)
    print('Max: {}, Min: {}'.format(data['temp_max'], data['temp_min']))
    print('---------------------------------------')

###########################################################################

def WriteCSV(data):
    with open('mael_weatherOpenMap.csv', 'a') as f:  # Just use 'w' mode in 3.x
        w = csv.DictWriter(f, data.keys())
        w.writeheader()
        w.writerow(data)

###############################################################################

def ReadCSV():
    try:
    #ouverture de fichier en mode lecture en specifiant le encodage
        with open("weatherOpenMap.csv",'r') as Fichier:
        #lecture – utilisation du parseur csv en specifiant délimiteur
            csv_contenu = csv.reader(Fichier,delimiter=",") 
            reader = csv.DictReader(Fichier)
            dic={}
            for row in reader:
                print (row['city'])
                dic.update(row)
            #fermeture du fichier avec la méthode close()
            Fichier.close()
            return dic
    except IOError:
        print("Fichier n'est pas trouvé")

##################################################################################

def getVilles():
    with open('city.list.json') as f:
        d = json.load(f)
        villes=pd.DataFrame(d)
        return villes

villes = getVilles()
villes_france = villes[villes["country"]=='FR']['id']
#############################################################################

if __name__ == '__main__':
    try:
        city_name=''
        country='FR'
        request_number = 0
        for ville in villes_france.iloc[0:500]:
            if request_number > 58:
                print('Quota de requêtes/minute en approche, sleep 1min1s')
                time.sleep(61)
                request_number = 0
            city_id = ville
            #Generation de l url
            print(colored('Generation de l url ', 'red',attrs=['bold']))
            url=url_builder(city_id,city_name,country)
            
            #Invocation du API afin de recuperer les données
            print(colored('Invocation du API afin de recuperer les données', 'red',attrs=['bold']))
            data=data_fetch(url)
            
            #Formatage des données
            print(colored('Formatage des donnée', 'red',attrs=['bold']))
            data_orgnized=data_organizer(data)
            
            #Affichage de données
            print(colored('Affichage de données ', 'red',attrs=['bold']))
            data_output(data_orgnized)

            
            #Enregistrement des données à dans un fichier CSV 
            print(colored('Enregistrement des données à dans un fichier CSV ', 'green',attrs=['bold']))
            WriteCSV(data_orgnized)
            
            #Lecture des données a partir de fichier CSV 
            #data=ReadCSV()
            #print(colored('Affichage des données lues de CSV ', 'green',attrs=['bold']))
            
            
            #Affichage des données 
            #data_output(data)
            
            
            
            request_number += 1

         
    except IOError:
        print('no internet')

#france_df = pd.read_csv('weatherOpenMap.csv')
#france_df = france_df[france_df['temp_max']!='temp_max']
#france_df.to_csv('clean_weather_France.csv')

print('Scrapping finished.')

while True:

    print('start : %s' % time.ctime())
    time.sleep(15000)

print('End: %s' % time.ctime())