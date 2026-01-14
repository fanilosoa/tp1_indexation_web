import json
from index_utils import normaliser_feature, charger_tous_index, charger_synonymes
from collections import defaultdict

# Traitement de la requête: tokenization, normalisation, synonymes)
def traiter_requete(requete, synonymes):
    """
    Tokenize + Normalise + Augmente synonymes origine
    
    Ex: "fr italy cotton" -> ['france', 'f', 'fr', 'italy', 'italia', 'cotton']
    """
    # Tokenization + normalisation
    tokens = normaliser_feature(requete)
    
    # Augmentation synonymes avec origin_synonyms.json
    tokens_augmente = []
    for token in tokens:
        tokens_augmente.append(token)  # Token original
        if token in synonymes:        # Si synonymes origine
            tokens_augmente.extend(synonymes[token])
    
    return list(set(tokens_augmente))  # pas de doublons

def filtre_au_moins_un_token(tokens, tous_index):
    """
    Retourne docs contenant au moins 1 des tokens
    """
    docs_candidats = set()
    
    for token in tokens:
        for nom_index, index in tous_index.items():
            if token in index:
                docs_candidats.update(index[token])
    
    print(f"   -> {len(tokens)} tokens -> {len(docs_candidats)} docs candidats")
    return list(docs_candidats)

def charger_stopwords(chemin="data/stopwords_nltk.json"):
    with open(chemin, 'r') as f:
        return set(json.load(f))


def filtre_tous_tokens_sauf_stopwords(tokens, docs_candidats, tous_index, stopwords):
    docs_finaux = set()
    tokens_essentiels = [t for t in tokens if t not in stopwords]
    print(f"   -> Tokens essentiels: {tokens_essentiels}") # tokens qui ne sont pas des stopwords
    
    for doc_url in docs_candidats:
        doc_match = True
        
        # Vérifie chaque token essentiel dans tous les index
        for token in tokens_essentiels:
            token_present = False
            for nom_index, index in tous_index.items():
                if token in index and doc_url in index[token]:
                    token_present = True
                    break
            
            if not token_present:
                doc_match = False
                break
        
        if doc_match:
            docs_finaux.add(doc_url)
    
    print(f"   -> {len(docs_candidats)} candidats -> {len(docs_finaux)} docs finaux")
    return list(docs_finaux)



# Pipeline de filtrage
def filtrer_documents(requete, tous_index, synonymes, chemin_stopwords="data/stopwords_nltk.json"):
    print(f"\n Filtrage : '{requete}'")
    
    tokens = traiter_requete(requete, synonymes)
    print(f"   -> Tokens: {tokens}")
    
    stopwords = charger_stopwords(chemin_stopwords)
    docs_candidats = filtre_au_moins_un_token(tokens, tous_index)
    docs_finaux = filtre_tous_tokens_sauf_stopwords(tokens, docs_candidats, tous_index, stopwords)
    
    return docs_finaux

# Test partie 2
def tester_partie2():
    """Teste filtrage complet"""
    print("=== TEST PARTIE 2 ===")
    
    # Charger Partie 1
    tous_index = charger_tous_index("input")
    synonymes = charger_synonymes("input/origin_synonyms.json")
    
    # Tests requêtes
    requetes_test = [
        "cotton", 
        "chocolate",
        "hershey chocolate",
        "orange italy",
        "cherry large"
    ]
    
    for requete in requetes_test:
        docs = filtrer_documents(requete, tous_index, synonymes)
        print(f"   -> '{requete}' -> {len(docs)} documents")
    
    print("\n Filtrage terminé")
    return True

if __name__ == "__main__":
    tester_partie2()
