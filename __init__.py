from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
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

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")


###
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

@app.route('/commits/')
def commits():
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
    except urllib.error.HTTPError:
        return "Erreur lors de la récupération des données depuis l'API GitHub"

    commits_per_minute = {}

    for commit in data:
        date_string = commit['commit']['author']['date']
        minutes = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ').minute
        commits_per_minute[minutes] = commits_per_minute.get(minutes, 0) + 1

    minutes = list(commits_per_minute.keys())
    commit_counts = list(commits_per_minute.values())

    return render_template('commits.html', minutes=minutes, commit_counts=commit_counts)
###

if __name__ == "__main__":
  app.run(debug=True)
