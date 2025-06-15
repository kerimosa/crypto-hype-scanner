# Fichier: test_google.py
from googlesearch import search
from bs4 import BeautifulSoup
import requests
import time

def google_crypto_scan(query, num_results=20):
    """
    Scanne les résultats de recherche Google pour trouver des pages pertinentes sur de nouvelles cryptos.
    """
    print(f"--- Lancement du scan Google pour la requête : '{query}' ---")
    
    # On ajoute un User-Agent pour avoir l'air d'un vrai navigateur
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    # Mots-clés pour qualifier une page comme étant "intéressante"
    keywords_to_find = ['tokenomics', 'airdrop', 'contract address', 'presale', 'whitepaper']

    try:
        # On cherche les URLs sur Google. Le 'sleep_interval' est une politesse pour ne pas spammer Google.
        links = list(search(query, num_results=num_results, sleep_interval=2))
        print(f"{len(links)} URLs trouvées. Analyse en cours...")
    except Exception as e:
        print(f"Erreur lors de la recherche Google : {e}. Votre IP est peut-être temporairement bloquée.")
        return []

    results = []
    for i, url in enumerate(links):
        print(f"  -> Analyse de l'URL {i+1}/{len(links)} : {url}")
        try:
            # On visite la page
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            # On parse le HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text().lower()

            # On vérifie si un de nos mots-clés est dans le texte
            if any(keyword in text for keyword in keywords_to_find):
                print("    --> PAGE PERTINENTE TROUVÉE !")
                # On récupère le titre de la page, c'est souvent plus utile
                title = soup.title.string if soup.title else "Pas de titre"
                results.append({'url': url, 'title': title})
            
            # On attend un peu avant de visiter la page suivante
            time.sleep(1)

        except Exception as e:
            print(f"    -> Erreur sur {url} : {e}")
            continue
    
    return results

if __name__ == "__main__":
    # Une requête plus précise utilisant les opérateurs de Google
    # "site:twitter.com" pour chercher uniquement sur Twitter/X
    # "intitle:" pour chercher dans le titre
    # On peut combiner plusieurs requêtes
    queries = [
        '"new token" "contract address" site:medium.com',
        'intitle:"airdrop" intitle:"token" since:2024-05-20'
    ]

    for q in queries:
        found_results = google_crypto_scan(query=q)
        
        if found_results:
            print(f"\n--- RÉSULTATS POUR '{q}' ---")
            for res in found_results:
                print(f"🔗 Titre : {res['title']}")
                print(f"   URL   : {res['url']}")
            print("-" * 50)
