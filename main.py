# Fichier: main.py (Version Corrigée)
import asyncio  # CHANGEMENT ICI: On importe la librairie pour gérer l'asynchrone
from scripts.notifier import send_message
from scripts.dex_scanner import find_new_solana_pairs

# CHANGEMENT ICI: La fonction principale est maintenant "async def"
async def run_scan():
    # CHANGEMENT ICI: On utilise "await" car send_message est maintenant une coroutine
    await send_message(" Démarrage du scan quotidien...")
    
    # La fonction find_new_solana_pairs n'a pas besoin de "await" car elle utilise "requests",
    # qui est une librairie synchrone. C'est normal.
    new_pairs = find_new_solana_pairs()
    
    if not new_pairs:
        # CHANGEMENT ICI: On utilise "await"
        await send_message("Scan terminé. Aucune nouvelle paire intéressante trouvée aujourd'hui.")
        return
        
    report_parts = [f" *Rapport du Scan : {len(new_pairs)} candidats trouvés !*"]
    for pair in new_pairs[:10]:
        part = (
            f"\n\n--- \n"
            f"**{pair['name']} (${pair['symbol']})**\n"
            f" Liquidité: `${pair['liquidity']:,.0f}`\n"
            f"[Voir sur DexScreener]({pair['url']})"
        )
        report_parts.append(part)
        
    final_report = "".join(report_parts)
    # CHANGEMENT ICI: On utilise "await"
    await send_message(final_report)
    print("Rapport envoyé sur Telegram.")

# CHANGEMENT ICI: C'est la nouvelle façon de lancer un script asynchrone
if __name__ == "__main__":
    asyncio.run(run_scan())
