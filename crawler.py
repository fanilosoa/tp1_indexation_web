from utils import get_html, is_allowed, parse_html, is_product_url
from collections import deque


START_URL = "https://web-scraping.dev/products"
MAX_PAGES = 50

def run_crawler(start_url: str, max_pages: int) -> None:
    """
    Permet de lancer le crawler
    """
    print(f"Vérification robots.txt pour {start_url}")

    if not is_allowed(start_url):
        print("Page interdite par robots.txt")
        return
    
    print("Page autorisée, récupération du HTML...")
    html = get_html(start_url)

    if html is None:
        print("Impossible de récupérer la page de départ.")
        return
    
    print("Parsing du HTML...")
    page_data = parse_html(html, start_url)

    if page_data:
        print(f" Titre: {page_data['title']}")
        print(f" Premier paragraphe: {page_data['first_paragraph']}")
        print(f" {len(page_data['links'])} liens internes trouvés")
        print(f" Exemples de liens: {page_data['links'][:3]}")
    else:
        print(" Erreur lors du parsing")

if __name__ == "__main__":
    run_crawler(START_URL, MAX_PAGES)
