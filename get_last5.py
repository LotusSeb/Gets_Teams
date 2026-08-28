"""
ÉTAPE ISOLÉE - Récupérer les 5 derniers matchs d'UNE équipe (test avec LOSC)
"""

import os
import requests
from team_mapping import MPP_TO_API_ID

api_token = os.environ.get('FOOTBALL_API_TOKEN', '')
headers = {'X-Auth-Token': api_token}

# Test avec LOSC
team_name = "LOSC"
team_id = MPP_TO_API_ID[team_name]

print(f"🚀 Récupération des 5 derniers matchs de {team_name} (ID {team_id})")

url = f'https://api.football-data.org/v4/teams/{team_id}/matches?status=FINISHED&limit=5'
response = requests.get(url, headers=headers, timeout=10)
print(f"Statut: {response.status_code}")

if response.status_code == 200:
    matches = response.json().get('matches', [])
    print(f"\n✅ {len(matches)} matchs trouvés:\n")
    
    for m in matches:
        home = m['homeTeam']['name']
        away = m['awayTeam']['name']
        home_score = m['score']['fullTime']['home']
        away_score = m['score']['fullTime']['away']
        date = m['utcDate'][:10]
        print(f"   {date} | {home} {home_score}-{away_score} {away}")
else:
    print(f"❌ Erreur: {response.text}")
