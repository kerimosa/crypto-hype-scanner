# Fichier: google_twitter_scanner.py
# Un script autonome pour scanner Twitter/X en utilisant Google comme intermédiaire.

from googlesearch import search
from bs4 import BeautifulSoup
import requests
import time

def scan_twitter_via_google(token_symbol, token_name, num_results=15):
    """
    Cherche des mentions d'un token sur Twitter en passant par une recherche Google ciblée.
    """
    # --- LA REQUÊTE GOOGLE MAGIQUE ---
    # On cherche le nom, le symbole et le cashtag, mais UNIQUEMENT sur twitter.com
    # On ajoute "since:AAAA-MM-JJ" pour ne chercher que les résultats récents.
    # Pour le test, on va chercher la dernière semaine.
    from datetime import datetime, timedelta
    one_week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    query = f'"{token_name}" OR {token_symbol} OR ${token_symbol} site:twitter.com OR site:x.com since:{one_week_ago}'
    
    print(f"--- Lancement du scan Twitter via Google ---")
    print(f"Requête Google : '{query}'")

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    found_tweets = []

    try:
        # On lance la recherche Google
        links = list(search(query, num_results=num_results, sleep_interval=2))
        print(f"\n{len(links)} liens Twitter trouvés par Google. Analyse des pages...")
    except Exception as e:
        print(f"Erreur lors de la recherche Google : {e}. IP peut-être bloquée.")
        return []

    for i, url in enumerate(links):
        print(f"  -> Analyse du lien {i+1}/{len(links)}: {url}")
        try:
            # On visite la page du tweet
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            # On utilise BeautifulSoup pour extraire le titre de la page.
            # Le titre d'une page de tweet contient souvent le texte du tweet lui-même.
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Le titre d'une page de tweet ressemble à : "Elon Musk on X: "Le texte du tweet...""
            title = soup.title.string if soup.title else "Titre non trouvé"
            
            # On nettoie un peu le titre pour ne garder que le texte pertinent
            if ' on X: "' in title:
                tweet_text = title.split(' on X: "')[1].rsplit('"', 1)[0]
            else:
                tweet_text = title

            found_tweets.append({'link': url, 'text': tweet_text})
            time.sleep(1) # Politesse

        except Exception as e:
            print(f"    -> Erreur en analysant l'URL {url}: {e}")
            continue
            
    return found_tweets

if __name__ == "__main__":
    # --- TESTONS AVEC UN TOKEN CONNU ---
    TOKEN_TO_TEST_SYMBOL = "WIF"
    TOKEN_TO_TEST_NAME = "dogwifhat"

    results = scan_twitter_via_google(TOKEN_TO_TEST_SYMBOL, TOKEN_TO_TEST_NAME)

    if results:
        print(f"\n--- {len(results)} TWEETS PERTINENTS TROUVÉS ---")
        for tweet in results:
            print("\n-------------------------------------------")
            print(f"🔗 Lien : {tweet['link']}")
            print(f"💬 Texte (extrait du titre) : {tweet['text']}")
            print("-------------------------------------------")
    else:
        print("\nAucun tweet pertinent trouvé via Google pour ce token.")
