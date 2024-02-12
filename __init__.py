from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
import requests
                                                                                                                                       
app = Flask(__name__) 
@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm

@app.route('/paris/')
def meteo():
    response = urlopen('https://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&cnt=16&appid=bd5e378503939ddaee76f12ad7a97608')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('temp', {}).get('day') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/histogramme/")
def mongraphique():
    return render_template("graphique.html")


# Fonction pour extraire les minutes à partir d'une chaîne de date formatée
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

# Fonction pour récupérer les commits depuis l'API GitHub et compter les commits par minute
@app.route('/commits/')
def commits():
    # Récupération des données de l'API GitHub
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = requests.get(url)
    commits_data = response.json()

    # Initialisation du dictionnaire pour stocker le nombre de commits par minute
    commits_per_minute = {}

    # Parcours des commits pour compter les commits par minute
    for commit in commits_data:
        date_string = commit['commit']['author']['date']
        response = requests.get(f"http://localhost:5000/extract-minutes/{date_string}")
        minutes = response.json()['minutes']
        commits_per_minute[minutes] = commits_per_minute.get(minutes, 0) + 1

    return render_template('commits.html', commits_per_minute=commits_per_minute)

if __name__ == "__main__":
  app.run(debug=True)
