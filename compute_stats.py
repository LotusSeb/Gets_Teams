"""
ETAPE ISOLEE - Calculer les stats par equipe a partir des derniers matchs
(buts marques et encaisses en moyenne)
"""

import os
import requests
import time
from team_mapping import MPP_TO_API_ID

api_token = os.environ.get('FOOTBALL_API_TOKEN', '')
headers = {'X-Auth-Token': api_token}

print("Calcul des stats par equipe\n")

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
        "nb_matches": len(matches),
        "avg_scored": round(avg_scored, 2),
        "avg_conceded": round(avg_conceded, 2)
    }

# Test avec quelques equipes d'abord
test_teams = ["LOSC", "Paris SG", "Angers SCO"]

stats = {}
for team_name in test_teams:
    team_id = MPP_TO_API_ID[team_name]
    
    # Recupere le nom complet API (necessaire pour identifier domicile/exterieur)
    url = f'https://api.football-data.org/v4/teams/{team_id}'
    response = requests.get(url, headers=headers, timeout=10)
    team_full_name = response.json().get('name', team_name)
    time.sleep(6)
    
    result = get_team_stats(team_id, team_full_name)
    stats[team_name] = result
    
    if result:
        print(f"{team_name}: {result['nb_matches']} match(s) | Buts marques: {result['avg_scored']} | Buts encaisses: {result['avg_conceded']}")
    else:
        print(f"{team_name}: aucune donnee")
    
    time.sleep(6)

print("\nTermine!")
