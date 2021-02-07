from flask import Flask, flash, redirect, render_template, \
     request, url_for, session
import dash
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html

from . import graph
from . import app
from bson import json_util
from . import scrapping
import pymongo
import json

###
#Ce fichier nous permet de créer les différentes routes que le site va avoir
###

#On declare une nouvelle notre base de donnée pour pouvoir l'utiliser et récupérer nos données
client = pymongo.MongoClient()
database = client['PSG']
collection_joueurs = database['Joueurs']
collection_resultats = database['Résultats']
collection_palmares = database['Palmares']
collection_calendrier = database['Calendrier']
collection_info = database['Info']

#On instancie notre application dash qui va nous permettre de créer notre page contenant les graphiques
#Le contenu de l'application dash se trouve dans le fichier graph.py
dash_app = dash.Dash(__name__, server=app, routes_pathname_prefix= '/dash/')
graph.GraphDash(dash_app=dash_app)

#Dans nos app.route on créer notre fonction qui va nous permettre de charger les données souhaitées et on retourne le fichier html qui correspond à la bonne page
@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/joueurs')
def joueurs():
    l_joueurs = list(collection_joueurs.find({}))
    
    return render_template('joueurs 1.html', l_joueurs=l_joueurs)

@app.route('/palmares')
def palmares():
    l_palmares = list(collection_palmares.find({}))
    return render_template('palmares.html', l_palmares=l_palmares)

@app.route('/resultats')
def resultats():
    l_resultats = list(collection_resultats.find({}))
    return render_template('resultats.html', l_resultats=l_resultats)

@app.route('/calendrier')
def calendrier():
    l_calendrier = list(collection_calendrier.find({}))
    return render_template('calendrier.html', l_calendrier=l_calendrier)

@app.route('/statistiques')
def statistiques():
    return render_template('stat.html')


#Met en route l'application dash
if __name__=='__main__':
     app.run(debug=True)