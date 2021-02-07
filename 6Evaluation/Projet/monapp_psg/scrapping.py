import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import pymongo

###
#Ce fichier va nous permettre de faire notre scraping. J'ai choisi de scraper les données sur Wikipédia et 
#via une API.
###

url = 'https://fr.wikipedia.org/wiki/Paris_Saint-Germain_Football_Club'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

#Scrape les infos générales sur le psg
tables = pd.read_html(url)
infos_generals = tables[0]
infos_generals[1][1] = '1904 ou 1970'
infos_generals.rename(columns={0:'0',1:'1'},inplace=True)

#Scrape le nom des joueurs du psg avec leur caractéristiques ("Numero,Poste,Nationnalité...")
joueurs_table = soup.find("table", attrs={"class": "toccolours"})
joueurs_table_data = joueurs_table.tbody.find_all("tr") 


headings = []
for th in joueurs_table_data[1].find_all("th"):
    headings.append(th.text.replace('\n', ' ').strip())
    
data = {}
for table in joueurs_table_data[1].find_all("table"):
    t_headers = []
    for th in table.find_all("th"):
        t_headers.append(th.text.replace('\n', ' ').strip())
    table_data = []
    for tr in table.tbody.find_all("tr"):
        t_row = {}

        for td, th in zip(tr.find_all("td"), t_headers): 
            t_row[th] = td.text.replace('\n', '').strip()
        table_data.append(t_row)
    data = table_data

#Création d'un DataFrame avec les données qu'on vient de scraper    
df_joueurs = pd.DataFrame([elt for elt in data if elt]) 

df_joueurs.rename(columns= {'Sélection[239]' : 'Sélection', 'P.' : 'Poste', 'No' : '_Numero' }, inplace = True)
df_joueurs.drop(['Nat.[238]'], axis='columns', inplace = True)
df_joueurs['Nationalité'] = df_joueurs['Sélection']
df_joueurs['Nationalité'][2] = 'France'
df_joueurs['Nationalité'][8] = 'France'
df_joueurs['Nationalité'][10] = 'Pays-Bas'
df_joueurs['Nationalité'][11] = 'France'
df_joueurs['Nom'][0] = 'Keylor Navas'
df_joueurs['Nom'][1] = 'Sergio Rico' 
df_joueurs['Nom'][2] = 'Alexandre Letellier'
df_joueurs['Nom'][3] = 'Presnel Kimpembe'
df_joueurs['Nom'][4] = 'Thilo Kehrer'
df_joueurs['Nom'][5] = 'Marquinhos'
df_joueurs['Nom'][6] = 'Juan Bernat'
df_joueurs['Nom'][7] = 'Layvin Kurzawa'
df_joueurs['Nom'][8] = 'Abdou Diallo'
df_joueurs['Nom'][9] = 'Alessandro Florenzi'
df_joueurs['Nom'][10] = 'Mitchel Bakker'
df_joueurs['Nom'][11] = 'Colin Dagba'
df_joueurs['Nom'][12] = 'Marco Verratti'
df_joueurs['Nom'][13] = 'Leandro Paredes'
df_joueurs['Nom'][14] = 'Ángel Di María'
df_joueurs['Nom'][15] = 'Rafinha'
df_joueurs['Nom'][16] = 'Danilo Pereira'
df_joueurs['Nom'][17] = 'Pablo Sarabia'
df_joueurs['Nom'][18] = 'Ander Herrera'
df_joueurs['Nom'][19] = 'Julian Draxler'
df_joueurs['Nom'][20] = 'Idrissa Gueye'
df_joueurs['Nom'][21] = 'Kylian Mbappé'
df_joueurs['Nom'][22] = 'Mauro Icardi'
df_joueurs['Nom'][23] = 'Neymar Jr'
df_joueurs['Nom'][24] = 'Moise Kean'
df_joueurs = df_joueurs.replace('G','Gardien').replace('D','Défenseur').replace('M', 'Milieu').replace('A', 'Attaquant')

table_palmares = soup.find('table', {'class' : 'wikitable centre'})

#Scrape le palmares du psg
champion_de_france = []
for i in table_palmares.find('li').find('li').find_all('a'):
    champion_de_france.append(i.text)
    
del champion_de_france[-1]
champion_de_france = champion_de_france + ['','','','']



vice_champion_de_france = []
for i in table_palmares.find('li').find_all('li')[1].find_all('a'):
    vice_champion_de_france.append(i.text)

del vice_champion_de_france[2]

Coupe_de_France_V =[]
for i in table_palmares.find_all('li')[5].find_all('a'):
    Coupe_de_France_V.append(i.text)
print(len(Coupe_de_France_V))

Coupe_de_France_F =[]
for i in table_palmares.find_all('li')[6].find_all('a'):
    Coupe_de_France_F.append(i.text)
    
Coupe_de_la_ligue_V =[]
for i in table_palmares.find_all('li')[11].find_all('a'):
    Coupe_de_la_ligue_V.append(i.text)
Coupe_de_la_ligue_V = Coupe_de_la_ligue_V + ['','','','']


Coupe_de_la_ligue_F =[]
for i in table_palmares.find_all('li')[12].find_all('a'):
    Coupe_de_la_ligue_F.append(i.text)

Trophée_des_champions_V =[]
for i in table_palmares.find_all('li')[7].find('li').find_all('a'):
    Trophée_des_champions_V.append(i.text)
Trophée_des_champions_V = Trophée_des_champions_V + ['','','']


Trophée_des_champions_F =[]
for i in table_palmares.find_all('li')[7].find_all('li')[1].find_all('a'):
    Trophée_des_champions_F.append(i.text)

Dict_palmares = {'Compétitions nationales' : {'Ligue 1' : {'champion de france': champion_de_france,'vice_champion_de_france' : vice_champion_de_france},
                                              'Ligue 2' : {'champion' : '1971'},
                                              'Coupe de france' : {'Vainqueur' : Coupe_de_France_V,'Finaliste' : Coupe_de_France_F},
                                              'Coupe de la ligue' : {'Vainqueur' : Coupe_de_la_ligue_V,'Finaliste' : Coupe_de_la_ligue_F},
                                              'Trophée des champions' : {'Vainqueur' : Trophée_des_champions_V,'Finaliste' : Trophée_des_champions_F}},
                 'Compétitions internationales' : {'Ligue des champions' : {'Finaliste' : '2020','Demi-finalistes':'1995'},
                                              "Coupe d'europe des vainqueurs de coupe" : {'Vainqueur' : '1996','Finaliste' : '1997'},
                                              'Ligue Europa' : {'Demi-finaliste': '1993'},
                                              "SuperCoupe de l'UEFA" : {'Finaliste': '1996'},
                                              'Coupe Intertoto' : {'Vainqueur': '2001'}}}

dict_palmares = {'Ligue 1' : champion_de_france,
                'Ligue 1 F' : vice_champion_de_france,
                'C_D_F' : Coupe_de_France_V,
                'C_D_F_F' : Coupe_de_France_F,
                'C_D_L' : Coupe_de_la_ligue_V,
                'C_D_L_F' : Coupe_de_la_ligue_F,
                'T_D_C' : Trophée_des_champions_V,
                'T_D_C_F' : Trophée_des_champions_F}
        
d_p = pd.DataFrame({'Ligue 1' : champion_de_france, 'C_D_F' : Coupe_de_France_V, 'C_D_L' : Coupe_de_la_ligue_V, 'T_D_C' : Trophée_des_champions_V})

headers = { 'X-Auth-Token': '823dceddc2cf40e09e781d56725c7b58' }

response = requests.get('https://api.football-data.org/v2/teams/524/matches?status=FINISHED', headers=headers) # 
result = json.loads(response.text)

response2 = requests.get('https://api.football-data.org/v2/teams/524/matches?status=SCHEDULED', headers=headers) # 
result2 = json.loads(response2.text)

date_match = []
score = []
competition = []
#Scrape les résultats des matchs du psg 
for i in result['matches']:
    date_match.append(i['utcDate'][0:10])
    score.append(i['homeTeam']['name']+' '+str(i['score']['fullTime']['homeTeam'])+' - '+ str(i['score']['fullTime']['awayTeam'])+' '+i['awayTeam']['name'])
    competition.append(i['competition']['name'])

date_match = date_match[::-1]
score = score[::-1]
competition = competition[::-1]
df_résultats = pd.DataFrame({'Date du matche' : date_match, 'Score' : score , 'Competition' : competition})

date_match2 = []
score2 = []
competition2 = []

#Scrape le calendrier du psg
for i in result2['matches']:
    date_match2.append(i['utcDate'][0:10])
    score2.append(i['homeTeam']['name']+' - '+i['awayTeam']['name'])
    competition2.append(i['competition']['name'])

df_calendrier = pd.DataFrame({'Date du matche' : date_match2, 'Equipe' : score2 , 'Competition' : competition2})
df_calendrier


#Récupération de données sur les statistiques des joueurs (Nombre de but,Nombre de match, Cartons..)
df_stat = pd.read_csv('Datapsg.csv',index_col=0)
df_stat = df_stat.rename(columns={'Joueur' : 'Nom'})
df_joueurs = pd.merge(df_joueurs,df_stat, on=['Nom'])

#Création d'une base de donnée Mongo pour stocker les données précedement scrapées
client = pymongo.MongoClient()
database = client['PSG']
collection_joueurs = database['Joueurs']
collection_résultats = database['Résultats']
collection_palmares = database['Palmares']
collection_calendrier = database['Calendrier']
collection_info = database['Info']

document_joueurs = df_joueurs.to_dict(orient = 'records')
document_résultats = df_résultats.to_dict(orient = 'records')
document_calendrier = df_calendrier.to_dict(orient = 'records')
document_palmares = d_p.to_dict(orient = 'records')
document_info = infos_generals.to_dict(orient = 'records')

#La méthode delete_many est un peu brute mais cela permet d'être sûr de ne pas empiler les mêmes données plusieurs fois
collection_joueurs.delete_many({})
collection_joueurs.insert_many(document_joueurs)

collection_résultats.delete_many({})
collection_résultats.insert_many(document_résultats)

collection_palmares.delete_many({})
collection_palmares.insert_many(document_palmares)

collection_calendrier.delete_many({})
collection_calendrier.insert_many(document_calendrier)

collection_info.delete_many({})
collection_info.insert_many(document_info)