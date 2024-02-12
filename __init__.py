from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__) 
@app.route("/contact/")
def MaPremiereAPI():
    return "<h2>Ma page de contact</h2>"
                                                                                                                                       
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

from flask import Flask, render_template

app = Flask(__name__) 

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/histogramme/")
def histogramme():
    # Supposons que vous ayez déjà collecté les données de température dans une liste nommée "temperatures"
    temperatures = [15, 17, 18, 19, 20, 22, 24, 25, 23, 21, 20, 18, 17, 16, 15, 14]

    # Construction du script JavaScript pour le graphique d'histogramme
    script = """
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Jour', 'Température'],
          """
    for i, temp in enumerate(temperatures):
        script += "['Jour {}', {}],".format(i+1, temp)
    script += "

  
if __name__ == "__main__":
  app.run(debug=True)
