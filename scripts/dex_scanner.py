# Fichier: scripts/dex_scanner.py (Version Finale, Propre et Correcte)
import requests
import time
from datetime import datetime, timedelta, timezone

def find_new_pairs_on_chain(chain_name):
    print(f"\n--- Recherche sur {chain_name.upper()} ---")
    
    # Paramètres de filtrage que tu peux ajuster
    hours_to_search = 168
    min_volume_24h = 50000
    min_liquidity_usd = 10000

    time_threshold = datetime.now(timezone.utc) - timedelta(hours=hours_to_search)
    
    api_url = "https://api.dexscreener.com/latest/dex/search"
    params = {
        'q': f'chain:{chain_name} liquidity > {min_liquidity_usd} volume > {min_volume_24h}',
        'orderBy': 'pairCreatedAt',
        'order': 'desc'
    }
    
    print(f"  -> Appel API pour la chaîne '{chain_name}'...")

    try:
        response = requests.get(api_url, params=params, headers={'User-Agent': 'CryptoScannerBot/1.0'})
        response.raise_for_status()
        
        data = response.json()
        pairs_from_api = data.get('pairs', [])
        
        if not pairs_from_api:
            print("  -> Aucune paire récente avec activité trouvée sur cette chaîne.")
            return []

        print(f"  -> {len(pairs_from_api)} paires candidates reçues. Filtrage par date en cours...")

        all_found_pairs = []
        for pair in pairs_from_api:
            created_at_timestamp = pair.get('pairCreatedAt', 0) / 1000
            pair_creation_date = datetime.fromtimestamp(created_at_timestamp, tz=timezone.utc)

            if pair_creation_date > time_threshold:
                volume_24h = pair.get('volume', {}).get('h24', 0)
                all_found_pairs.append({
                    'chain': chain_name,
                    'name': pair.get('baseToken', {}).get('name', 'N/A'),
                    'symbol': pair.get('baseToken', {}).get('symbol', 'N/A'),
                    'liquidity': float(pair.get('liquidity', {}).get('usd', 0)),
                    'volume_24h': float(volume_24h),
                    'url': pair.get('url', '#')
                })
        
        print(f"--- Recherche terminée pour {chain_name.upper()}. Total final : {len(all_found_pairs)} paires ---")
        return all_found_pairs

    except Exception as e:
        print(f"  -> Erreur durant le scan de la chaîne {chain_name.upper()}: {e}")
        return []
