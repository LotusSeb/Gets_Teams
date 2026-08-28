"""
ETAPE ISOLEE - Appliquer la formule de prediction sur les stats calculees
"""

import os
import requests
import time
from team_mapping import MPP_TO_API_ID

api_token = os.environ.get('FOOTBALL_API_TOKEN', '')
headers = {'X-Auth-Token': api_token}


def get_team_full_name(team_id):
    url = f'https://api.football-data.org/v4/teams/{team_id}'
    response = requests.get(url, headers=headers, timeout=10)
    return response.json().get('name', '')


def get_team_stats(team_id, team_full_name):
    """Recupere les derniers matchs et calcule buts marques/encaisses en moyenne"""
    url = f'https://api.football-data.org/v4/teams/{team_id}/matches?status=FINISHED&limit=5'
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code != 200:
        return None
    
    matches = response.json().get('matches', [])
    if len(matches) == 0:
        return None
    
    goals_scored = []
    goals_conceded = []
    
    for m in matches:
        home_name = m['homeTeam']['name']
        home_score = m['score']['fullTime']['home']
        away_score = m['score']['fullTime']['away']
        
        if home_name == team_full_name:
            goals_scored.append(home_score)
            goals_conceded.append(away_score)
        else:
            goals_scored.append(away_score)
            goals_conceded.append(home_score)
    
    avg_scored = sum(goals_scored) / len(goals_scored)
    avg_conceded = sum(goals_conceded) / len(goals_conceded)
    
    return {
        "avg_scored": round(avg_scored, 2),
        "avg_conceded": round(avg_conceded, 2)
    }


def predict_score(team_home, team_away):
    """Applique la formule: Buts_Dom = (marques_dom + encaisses_ext) / 2"""
    id_home = MPP_TO_API_ID[team_home]
    id_away = MPP_TO_API_ID[team_away]
    
    name_home = get_team_full_name(id_home)
    time.sleep(6)
    name_away = get_team_full_name(id_away)
    time.sleep(6)
    
    stats_home = get_team_stats(id_home, name_home)
    time.sleep(6)
    stats_away = get_team_stats(id_away, name_away)
    time.sleep(6)
    
    if not stats_home or not stats_away:
        return None
    
    buts_dom = round((stats_home['avg_scored'] + stats_away['avg_conceded']) / 2)
    buts_ext = round((stats_away['avg_scored'] + stats_home['avg_conceded']) / 2)
    
    return {
        "home": team_home,
        "away": team_away,
        "stats_home": stats_home,
        "stats_away": stats_away,
        "pred_home": buts_dom,
        "pred_away": buts_ext
    }


# Test sur un seul match
print("Test de la formule sur Rennes vs Le Mans\n")

result = predict_score("Rennes", "Le Mans")

if result:
    print(f"Rennes: marque {result['stats_home']['avg_scored']} / encaisse {result['stats_home']['avg_conceded']}")
    print(f"Le Mans: marque {result['stats_away']['avg_scored']} / encaisse {result['stats_away']['avg_conceded']}")
    print(f"\nPrediction: Rennes {result['pred_home']} - {result['pred_away']} Le Mans")
else:
    print("Erreur: donnees manquantes")
