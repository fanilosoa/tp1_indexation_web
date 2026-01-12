import time
from urllib import request, error
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

# Délai de politesse en secondes entre deux requêtes
REQUEST_DELAY = 1.0

def make_request(url: str, user_agent: str = "FANILOSOA-TP1-Crawler") -> bytes | None:
    """
    Envoie une requête HTTP vers l'URL et renvoie le contenu brut,
    ou None en cas d'erreur.
    """
    # Politesse : attendre un peu entre deux requêtes
    time.sleep(REQUEST_DELAY)

    # Préparation de la requête avec un User-Agent
    req = request.Request(
        url,
        headers={"User-Agent": user_agent}
    )

    try:
        with request.urlopen(req, timeout=10) as response:
            # On renvoie le contenu brut (bytes)
            return response.read()
    except error.HTTPError as e:
        print(f"[HTTPError] {e.code} pour l'URL {url}")
    except error.URLError as e:
        print(f"[URLError] {e.reason} pour l'URL {url}")
    except Exception as e:
        print(f"[Erreur] {e} pour l'URL {url}")

    return None


def get_html(url: str, encoding: str = "utf-8") -> str | None:
    """
    Récupère le HTML d'une page sous forme de chaîne de caractères,
    ou None en cas d'erreur.
    """
    content = make_request(url)
    if content is None:
        return None

    try:
        return content.decode(encoding, errors="ignore")
    except Exception as e:
        print(f"[Erreur] impossible de décoder le contenu de {url}: {e}")
        return None
    
def get_robots_parser(base_url: str) -> RobotFileParser | None:
    """
    Récupère le parseur robots.txt pour le domaine de base_url.
    """
    # Construire l'URL du robots.txt
    parsed = urlparse(base_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    
    content = make_request(robots_url)
    if content is None:
        print(f"[INFO] Pas de robots.txt trouvé pour {robots_url}")
        return None
    
    rp = RobotFileParser()
    rp.set_url(robots_url)
    rp.parse(content.decode('utf-8').splitlines())
    return rp

def is_allowed(url: str, user_agent: str = "FANILOSOA-TP1-Crawler") -> bool:
    """
    Vérifie si le crawler a le droit de visiter l'URL selon robots.txt.
    """
    # Récupérer le parseur pour ce domaine
    parsed = urlparse(url)
    robots_parser = get_robots_parser(f"{parsed.scheme}://{parsed.netloc}/")
    
    # Si pas de robots.txt, on autorise tout
    if robots_parser is None:
        return True
    
    # Vérifier si on peut aller chercher cette URL
    return robots_parser.can_fetch(user_agent, url)

def parse_html(html: str, base_url: str) -> dict | None:
    """
    Parse le HTML et extrait : titre, premier paragraphe, liens internes.
    """
    soup = BeautifulSoup(html, 'lxml')
    
    # Extraction du titre: préférence <title>, sinon <h1>)
    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.get_text(strip=True)
    else:
        h1_tag = soup.find('h1')
        title = h1_tag.get_text(strip=True) if h1_tag else "Sans titre"
    
    # Premier paragraphe : le premier <p> non-vide dans le body
    first_p = soup.find('body')
    if first_p:
        first_p = first_p.find('p')
    if first_p:
        first_paragraph = first_p.get_text(strip=True)[:200] + "..."  # Limite à 200 caractères
    else:
        first_paragraph = "Aucun paragraphe trouvé"
    
    # Extraction des liens internes
    base_domain = urlparse(base_url).netloc
    links = []
    
    for link in soup.find_all('a', href=True):
        href = link['href']
        # Convertir en URL absolue
        absolute_url = urljoin(base_url, href)
        
        # Garder seulement les liens internes au même domaine
        if urlparse(absolute_url).netloc == base_domain:
            links.append(absolute_url)
    
    # Éliminer les doublons
    links = list(set(links))
    
    return {
        "title": title,
        "url": base_url,
        "first_paragraph": first_paragraph,
        "links": links
    }

def is_product_url(url: str) -> bool:
    """
    Retourne True si l'URL contient le token 'product'.
    """
    return 'product' in url.lower()

