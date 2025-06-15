# Fichier: scripts/social_analyzer.py (Version Finale, Propre et Correcte)
import os
import praw
from dotenv import load_dotenv

load_dotenv()

try:
    reddit_api = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
        check_for_async=False
    )
    print("Module Social Analyzer initialisé (connexion à Reddit OK).")
except Exception as e:
    reddit_api = None
    print(f"ERREUR: Impossible de se connecter à l'API Reddit: {e}")

def analyze_token_hype(token_symbol, token_name):
    if not reddit_api or not token_symbol:
        return {"mention_count": 0, "top_post_url": ""}

    search_query = f'"{token_name}" OR {token_symbol} OR ${token_symbol}'
    print(f"  -> Recherche Reddit pour : '{search_query}'")

    mention_count = 0
    top_post_score = -1
    top_post_url = ""

    try:
        search_results = reddit_api.subreddit("all").search(
            search_query,
            limit=100,
            time_filter='week',
            sort='new'
        )
        
        for post in search_results:
            mention_count += 1
            if post.score > top_post_score:
                top_post_score = post.score
                top_post_url = post.permalink

    except Exception as e:
        print(f"  -> Erreur durant la recherche Reddit : {e}")
        return {"mention_count": 0, "top_post_url": ""}

    if top_post_url:
        top_post_url = f"https://www.reddit.com{top_post_url}"
        
    print(f"  -> Trouvé {mention_count} mentions sur l'ensemble de Reddit.")
    return {"mention_count": mention_count, "top_post_url": top_post_url}
