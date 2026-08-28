"""
ÉTAPE ISOLÉE - Récupérer les derniers matchs (jusqu'à 5) pour TOUTES les équipes
"""

import os
import requests
import time
from team_mapping import MPP_TO_API_ID

api_token = os.environ.get('FOOTBALL_API_TOKEN', '')
headers = {'X-Auth-Token': api_token}

print("🚀 Récupération des derniers matchs pour toutes les équipes\n")

results = {}

for team_name, team_id in MPP_TO_API_ID.items():
    url = f'https://api.football-data.org/v4/teams/{team_id}/matches?status=FINISHED&limit=5'
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        matches = response.json().get('matches', [])
        results[team_name] = matches
        print(f"✅ {team_name}: {len(matches)} match(s) trouvé(s)")
        for m in matches:
            home = m['homeTeam']['name']
            away = m['awayTeam']['name']
            home_score = m['score']['fullTime']['home']
            away_score = m['score']['fullTime']['away']
            date = m['utcDate'][:10]
            print(f"      {date} | {home} {home_score}-{away_score} {away}")
    else:
        print(f"❌ {team_name}: erreur {response.status_code}")
        results[team_name] = []
    
    # Respecter les limites de l'API (10 req/min sur le plan gratuit)
    time.sleep(6)

print("\n✅ Terminé!")
