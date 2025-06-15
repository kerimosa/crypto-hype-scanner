# Fichier: main.py (Version Finale, Propre et Correcte)
import asyncio
from scripts.notifier import send_message
from scripts.dex_scanner import find_new_pairs_on_chain
from scripts.social_analyzer import analyze_token_hype

CHAINS_TO_SCAN = ["ethereum", "arbitrum", "optimism", "base", "solana", "bsc", "polygon_zkevm", "ton", "osmosis"]

async def run_scan():
    await send_message(" Démarrage du scan quotidien (On-Chain + Social)...")
    
    # Étape 1: Scan On-Chain
    all_found_pairs = []
    for chain in CHAINS_TO_SCAN:
        pairs_from_chain = find_new_pairs_on_chain(chain)
        all_found_pairs.extend(pairs_from_chain)
        await asyncio.sleep(0.5)
    
    if not all_found_pairs:
        await send_message("Scan terminé. Aucune nouvelle paire à fort volume trouvée aujourd'hui.")
        return

    # Étape 2: Analyse Sociale
    print("\n--- Démarrage de l'analyse sociale pour chaque candidat ---")
    analyzed_pairs = []
    for pair_data in all_found_pairs:
        print(f"Analyse de : {pair_data.get('name', 'N/A')} (${pair_data.get('symbol', 'N/A')})")
        
        social_data = analyze_token_hype(pair_data.get('symbol'), pair_data.get('name'))
        
        pair_data['mentions'] = social_data['mention_count']
        pair_data['social_link'] = social_data['top_post_url']
        
        analyzed_pairs.append(pair_data)
        await asyncio.sleep(0.5)

    # Étape 3: Tri et Reporting
    analyzed_pairs.sort(key=lambda x: (x['mentions'], x['volume_24h']), reverse=True)
    
    report_parts = [f" *Rapport Quotidien : {len(analyzed_pairs)} tokens analysés (triés par Hype & Volume)*"]
    
    for pair in analyzed_pairs[:10]:
        hype_indicator = f"🔥 {pair['mentions']} mentions" if pair['mentions'] > 0 else "Aucune mention"
        
        part = (
            f"\n\n--- \n"
            f"**{pair['name']} (${pair['symbol']})**\n"
            f" Chaîne: `{pair['chain'].upper()}`\n"
            f" Volume 24h: **${pair['volume_24h']:,.0f}** | Hype: {hype_indicator}\n"
            f" Liquidité: `${pair['liquidity']:,.0f}`\n"
            f"[Voir sur DexScreener]({pair['url']})"
        )
        if pair['social_link']:
            part += f" | [Voir le Top Post]({pair['social_link']})"
        report_parts.append(part)
        
    final_report = "".join(report_parts)
    await send_message(final_report)
    print("\nRapport final envoyé sur Telegram.")

if __name__ == "__main__":
    asyncio.run(run_scan())
