
###
#Ce fichier permet de créer des graphiques avec les différentes statistiques des joueurs
###

import plotly_express as px
import pandas as pd
import math
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output

#Récupération et traitement des données
df_stat = pd.read_csv('Datapsg.csv',index_col = 0)

df1 = df_stat[df_stat['Nb_but'] >= 5]
df2 = df_stat[df_stat['Carton_J'] >= 3]
df3 = df_stat[df_stat['Carton_J'] >= 1]




class GraphDash:   
    def __init__(self, dash_app):
        super().__init__()
        self.dash_app = dash_app

        #Création des graphiques avec plotly_express
        graph1 = px.bar(df1, y='Nb_but',x='Joueur',title='Les 5 meilleurs buteurs du Paris St Germain')
    
        graph2 = px.bar(df_stat, y='Nb_match',x='Joueur', color='Nb_but', title='Nombre de match de chaque joueur')


        self.dash_app.layout = html.Div(children=[

                            
                            dcc.Graph(
                                id='graph1',
                                figure=graph1
                            ),
                            

                            html.Div(children=f'''
                                Ce n'est pas étonnant que Kylian Mbappé soit le meilleur buteur du Paris St-Germain. Très en forme depuis le début de la saison, Mbappé est aujourd'hui 
                                le meilleur buteur de la Ligue 1 et figure parmis les meilleurs buteurs européens. Il a connu une petite baisse de régime cet hivers mais il revient en force depuis quelques semaines. Que va t-il nous réserver pour la suite de la saison ?
                                Grosse performance de Neymar Jr qui le est deuxième meilleur buteur du psg avtuellement sachant qu'il à loupé beaucoup de match avec sa blessure.
                            ''',style={'textAlign': 'center'}), #Créer une zone pour afficher du texte, c'est ici que nous mettons le commentaire du graphique en question

                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),


                            dcc.Graph( 
                                id='graph2',
                                figure=graph2
                            ),
                            

                            html.Div(children=f'''
                                Grosse surprise !! Mitchel Bakker jeune joueur Hollandais arrivé au PSG en 2019 est le joueur le plus utilisé de l'effectif. Il profite effectivement de la
                                blessure de Juan Bernat mais c'est un joueur très intéressant qui nous surprend de jour en jour. À noter qu'Ander Herrera est aussi très utilisé bien que nous connaissons la forte concurrence des joueurs du PSG
                                au milieu de terrain. Ils sont 9 milieus !! Le jeu de couleur est assez intéressant pour analyser le nombre de buts par match des joueurs en fonction du nombre de matchs joué 
                                dans la saison. Ces deux données sont plutôt bien corrélées. Nous remarquons qu'Mbappé qui est le meilleur buteur est également celui qui a joué le plus de match
                                parmis les attaquants. Le lien est donc plutôt logique. Neymar est le seul joueur à nous fausser cet hypothèse mais étant donner la forme de Neymar cette saison ce n'est pas 
                                surprenant. 

                            ''',style={'textAlign': 'center'}), #Créer une zone pour afficher du texte, c'est ici que nous mettons le commentaire du graphique en question

                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                        

                            html.Label('Nombre de cartons :',style={'color': 'black', 'fontSize': 20,'font-weight': 'bold'}),
                            dcc.Dropdown(
                            id="carton-dropdown",
                            options=[
                                {'label': 'Cartons Jaunes', 'value': 'Carton_J'},
                                {'label': 'Cartons Rouges', 'value': 'Carton_R'},
                                
                            ],
                            value='Carton_J',
                            ),    #Création d'une zone pour selectionner differentes variables qui vont nous permettre de changer les données d'un graphique et de le rendre interactif

                            dcc.Graph(
                                id='graph4',
                              
                            ),

                            html.Div(children=f'''
                                Pas de surprise du coté des cartons. Nous connaissons évidemment le caractère de nos joueurs comme Verratti, Paredes, Neymar ou encore notre SOLDAT Kimpembe !! 

                            ''',style={'textAlign': 'center'}),


        ]
        )

    #Création des callback qui vont nous permettre de récuperer les input créés dans les Dropdown et modifier les graphiques en fonction de la variable choisie.
    #Ce sont les dropdown et les callback qui nous permette de créer des graphiques interactifs 

        @self.dash_app.callback(
        Output('graph4','figure'), 
        [Input('carton-dropdown','value')] 
        )
        def carton(x):
            graph4 = px.bar(df3, x=x,y='Joueur', color='Nb_match')
            return graph4
