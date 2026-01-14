import json
import os
import nltk
from nltk.corpus import stopwords

# Chargement des index
def charger_tous_index(dossier_data="input"):
    """
    Charge les 6 index -> dict{nom: index}
    
    Retourne : {
        'brand': index_brand,
        'title': index_title,
        'description': index_desc,
        'origin': index_origin,
        'reviews': index_reviews
    }
    """
    index_files = {
        'brand': 'brand_index.json',
        'title': 'title_index.json', 
        'description': 'description_index.json',
        'origin': 'origin_index.json',
        'reviews': 'reviews_index.json'
    }
    
    tous_index = {}
    for nom, fichier in index_files.items():
        chemin = os.path.join(dossier_data, fichier)
        tous_index[nom] = charger_index(chemin)
        print(f" {nom}: {len(tous_index[nom])} termes")
    
    return tous_index

# Chargement des synonymes et des products
def charger_index(chemin):
    """Charge 1 index json -> dict{token: [doc_ids]}"""
    try:
        with open(chemin, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f" Fichier {chemin} manquant !")
        return {}

def charger_synonymes(chemin):
    """Charge origin_synonyms.json"""
    return charger_index(chemin)

def charger_products(chemin):
    """Charge rearranged_products.jsonl -> dict{doc_id: infos}"""
    products = {}
    try:
        with open(chemin, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                doc = json.loads(line.strip())
                products[str(i)] = {
                    'titre': doc.get('title', ''),
                    'description': doc.get('description', ''),
                    'url': doc.get('url', doc.get('asin', f'doc_{i}')),
                    'features': doc.get('productfeatures', {})
                }
        print(f" {len(products)} produits chargés")
        return products
    except FileNotFoundError:
        print(f" Fichier {chemin} manquant !")
        return {}

# Normalisation
def normaliser_feature(valeur):
    if not valeur or not isinstance(valeur, str):
        return []
    
    valeur = str(valeur).lower()
    for c in ",.;:!?()[]{}\"'":
        valeur = valeur.replace(c, " ")
    
    tokens = [t.strip() for t in valeur.split()
              if len(t.strip()) > 2]
    return tokens

# Stopwords NLTK
def generer_stopwords(chemin_sortie="data/stopwords_nltk.json"):
    os.makedirs(os.path.dirname(chemin_sortie), exist_ok=True)
    nltk.download('stopwords', quiet=True)
    stops = stopwords.words('english')
    
    with open(chemin_sortie, 'w') as f:
        json.dump(stops, f)
    print(f" {len(stops)} stopwords sauvegardés -> {chemin_sortie}")
    return stops


# Test partie 1
def tester_partie1():
    print("=== TEST PARTIE 1 - 6 INDEX ===")
    
    # Chargement des 6 index
    print("\n1. Chargement 6 index")
    tous_index = charger_tous_index("input")
    
    # Test normaliser_feature()
    print("\n2. Test normalisation requête")
    tokens = normaliser_feature("Hershey's Italy Cotton")
    print(f"   -> 'Hershey's Italy Cotton' -> {tokens}")
    
    # Chargement de origin_synonyms.json
    print("\n3. Synonymes origine")
    synonymes = charger_synonymes("input/origin_synonyms.json")
    print(f"   -> {len(synonymes)} synonymes pays")
    if synonymes:
        print(f"   -> Ex: {list(synonymes.items())[:2]}")

    # Chargement de rearranged_products.jsonl
    print("\n4. rearranged_products.jsonl")
    products = charger_products("input/rearranged_products.jsonl")
    print(f"   -> {len(products)} documents disponibles")
    if products:
        print(f"   -> Ex doc_0: {list(products['0'].keys())}")
    
    # Stopwords
    print("\n5. Stopwords NLTK")
    generer_stopwords()
    
    print("\nChargement terminé")
    return {
        'tous_index': tous_index,
        'synonymes': synonymes,
        'products': products
    }

if __name__ == "__main__":
    tester_partie1()
