from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
  
@app.route('/')
def hello_world():
    return render_template('hello.html') #Commentaire

@app.route("/contact/")
def MaPremiereAPI():
    return render_template('contact.html')

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")

# Route pour extraire les minutes d'une date donnée
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

# Route pour afficher le graphique des commits par minute
@app.route('/commits/')
def commits_graph():
    # URL de l'API GitHub pour extraire les commits
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    
    # Effectuer la requête à l'API GitHub pour obtenir les commits
    response = requests.get(url)
    commits_data = response.json()

    # Extraire les minutes des dates de commit
    commit_minutes = []
    for commit in commits_data:
        commit_date = commit['commit']['author']['date']
        minutes = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ').minute
        commit_minutes.append(minutes)

    # Passer les minutes au template HTML pour afficher le graphique
    return render_template('commits.html', commit_minutes=commit_minutes)
  
if __name__ == "__main__":
  app.run(debug=True)
