# Fichier: scripts/dex_scanner.py (Nouvelle Version avec API de Recherche)
import requests
from datetime import datetime, timedelta, timezone

def find_new_solana_pairs():
    print("Recherche de nouvelles paires sur Solana (via API de recherche)...")
    
    # --- PARAMÈTRES DE RECHERCHE (tu peux les ajuster ici) ---
    # On cherche les paires créées il y a moins de 7 jours.
    # On remet des valeurs raisonnables pour commencer.
    days_to_search = 7
    min_liquidity_usd = 1000

    # On calcule la date de départ pour la recherche
    search_start_date = datetime.now(timezone.utc) - timedelta(days=days_to_search)
    # On la formate comme l'attend l'API (ex: 2024-05-20T10:00:00Z)
    formatted_date = search_start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    # On utilise l'endpoint de recherche. La requête est dans le 'q'.
    # On cherche les paires sur Solana, créées après notre date, avec une liquidité > min_liquidity
    api_url = (
        "https://api.dexscreener.com/latest/dex/search"
        f"?q=pairCreatedAt after {formatted_date} AND chain:solana AND liquidity > {min_liquidity_usd}"
    )

    print(f"URL de l'API utilisée : {api_url}")

    try:
        response = requests.get(api_url, headers={'User-Agent': 'CryptoScannerBot/1.0'})
        response.raise_for_status()  # Vérifie si l'API a retourné une erreur (4xx, 5xx)
        
        data = response.json()
        all_pairs = data.get('pairs', [])
        
        if not all_pairs:
            print("Aucune paire retournée par la recherche de l'API.")
            return []

        print(f"{len(all_pairs)} paires trouvées par l'API. Formatage en cours...")
        
        # Le filtrage est déjà fait par l'API, on n'a plus qu'à formater les résultats.
        formatted_pairs = []
        for pair in all_pairs:
            formatted_pairs.append({
                'name': pair.get('baseToken', {}).get('name', 'N/A'),
                'symbol': pair.get('baseToken', {}).get('symbol', 'N/A'),
                'liquidity': float(pair.get('liquidity', {}).get('usd', 0)),
                'url': pair.get('url', '#')
            })
        
        return formatted_pairs

    except requests.exceptions.HTTPError as e:
        print(f"ERREUR HTTP de l'API: {e.response.status_code} - {e.response.text}")
        return []
    except Exception as e:
        print(f"Une erreur inattendue est survenue: {e}")
        return []
