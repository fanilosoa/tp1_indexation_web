from utils import get_html, is_allowed, parse_html, is_product_url
from collections import deque
import json
from typing import List, Dict

def run_crawler(start_url: str, max_pages: int) -> List[Dict]:
    """
    Crawler principal avec file de priorité et arrêt à max_pages.
    """
    # Structures de données
    pages_visited = 0
    visited_urls = set()
    results = []  # Pour stocker les données
    
    # File de priorité : (priorité, url) où priorité=0 pour products, 1 sinon
    # Les petites priorités passent en premier
    priority_queue = deque()
    
    # Initialiser avec la page de départ
    priority_queue.append((0 if is_product_url(start_url) else 1, start_url))
    
    print(f"Démarrage du crawler depuis {start_url} (max {max_pages} pages)")
    
    while priority_queue and pages_visited < max_pages:
        # Récupérer l'URL avec la meilleure priorité
        priority, current_url = priority_queue.popleft()
        
        if current_url in visited_urls:
            continue
            
        print(f"[{pages_visited+1}/{max_pages}] Visite : {current_url}")
        visited_urls.add(current_url)
        
        # Vérifier robots.txt
        if not is_allowed(current_url):
            print(f"  Interdit par robots.txt")
            continue
        
        # Récupérer et parser
        html = get_html(current_url)
        if html is None:
            print(f"  Impossible de récupérer")
            continue
            
        page_data = parse_html(html, current_url)
        if page_data:
            results.append(page_data)
            pages_visited += 1
            print(f"  {page_data['title'][:50]}...")
        else:
            print(f"  Erreur parsing")
            continue
        
        # Ajouter les nouveaux liens à la file (avec priorité)
        for link in page_data['links']:
            if link not in visited_urls:
                priority = 0 if is_product_url(link) else 1
                priority_queue.append((priority, link))
        
        print(f"  File restante : {len(priority_queue)} URLs")
    
    print(f"\nCrawler terminé : {pages_visited} pages visitées")
    return results

def save_results_to_json(results: List[Dict], filename: str = "crawler_output.json") -> None:
    """
    Sauvegarde les résultats du crawler dans un fichier JSON.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f" Résultats sauvegardés dans {filename}")


if __name__ == "__main__":
    
    # Sauvegarde des 50 pages
    START_URL = "https://web-scraping.dev/products"
    MAX_PAGES = 50
    results = run_crawler(START_URL, MAX_PAGES)
    save_results_to_json(results)

    # Tests avec différentes pages de départ
    print("=== TEST 1: Page des apparel ===")
    results1 = run_crawler("https://web-scraping.dev/products?category=apparel", 10)
    save_results_to_json(results1, "test_apparel.json")

    print("\n=== TEST 2: Page des testimonials ==="),
    results2 = run_crawler("https://web-scraping.dev/testimonials", 10)
    save_results_to_json(results2, "test_testimonials.json")
