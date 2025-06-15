# Fichier: test_twitter.py (Version améliorée et plus robuste)
from ntscraper import Nitter
import time

# --- CONFIGURATION DU TEST ---
SEARCH_QUERY = '"dogwifhat" OR $WIF since:2024-05-20' # On change de sujet pour varier
MAX_TWEETS = 15

def run_twitter_test():
    """
    Lance un scan de test sur Twitter/X avec une gestion d'erreur améliorée.
    """
    print("--- Lancement du test de scraping Twitter/X (v2) ---")
    print(f"Recherche pour : {SEARCH_QUERY}")

    # On initialise le scraper. Le paramètre 'log_level=1' nous donnera plus d'infos en cas de problème.
    scraper = Nitter(log_level=1)

    try:
        # On lance la recherche
        search_results = scraper.get_tweets(SEARCH_QUERY, mode='term', number=MAX_TWEETS)
        
        # La structure de la réponse peut varier, on la vérifie plus attentivement
        if not search_results or 'tweets' not in search_results or not search_results['tweets']:
            print("\n--> Aucun tweet trouvé ou la réponse de l'instance est vide.")
            print("--> Cela peut être normal si la recherche ne donne rien, ou si l'instance Nitter a un problème.")
            return

        print(f"\n--- {len(search_results['tweets'])} Tweets trouvés ---")

        # On boucle sur chaque tweet trouvé pour afficher les infos
        for i, tweet in enumerate(search_results['tweets']):
            user = tweet.get('user', {}).get('name', 'N/A')
            username = tweet.get('user', {}).get('username', 'N/A')
            text = tweet.get('text', 'Texte non trouvé')
            link = tweet.get('link', '#')
            
            print(f"\n--- Tweet #{i+1} ---")
            print(f"De: {user} (@{username})")
            print(f"Tweet: {text}")
            print(f"Lien: {link}")
            
        print("\n--- Test terminé avec succès ! ---")

    except Exception as e:
        print(f"\nUNE ERREUR EST SURVENUE : {e}")
        print("Conseils de débogage :")
        print("1. Assurez-vous que 'ntscraper' est à jour (`pip install --upgrade ntscraper`).")
        print("2. Les instances Nitter peuvent être temporairement en panne. Réessayez plus tard.")
        print("3. Votre connexion internet ou votre IP est peut-être bloquée.")

if __name__ == "__main__":
    run_twitter_test()
