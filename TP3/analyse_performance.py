from index_utils import charger_tous_index, charger_synonymes, charger_products, charger_stopwords
from filtre import traiter_requete, filtre_au_moins_un_token, filtre_tous_tokens_sauf_stopwords
from ranking import rank_documents


JEUX_REQUETES = {
    "simples": ["italy", "chocolate", "cherry", "orange"],
    "multi": ["chocolate italy", "cherry large", "orange medium"],
    "synonymes": ["fr", "usa", "it"]
}

def etape1_jeu_requetes():
    print("=== ÉTAPE 1: JEU DE REQUÊTES TEST ===")
    
    tous_index = charger_tous_index("input")
    synonymes = charger_synonymes("input/origin_synonyms.json")
    products = charger_products("input/rearranged_products.jsonl")
    stopwords = charger_stopwords("data/stopwords_nltk.json")
    
    for categorie, requetes in JEUX_REQUETES.items():
        print(f"\n REQUÊTES - {categorie.upper()}")
        for req in requetes:
            tokens = traiter_requete(req, synonymes)
            tokens_essentiels = [t for t in tokens if t not in stopwords]
            docs_candidats = filtre_au_moins_un_token(tokens, tous_index, False)
            docs_finaux = filtre_tous_tokens_sauf_stopwords(tokens, docs_candidats, tous_index, stopwords, False)
            ranked = rank_documents(docs_finaux, tokens_essentiels, tous_index, products, top_k=3)
            
            print(f"   '{req}' -> {len(docs_candidats)} candidats -> {len(docs_finaux)} documents finaux")

def etape2_scores_ranking():
    print("\n === ÉTAPE 2: ANALYSE SCORES RANKING ===")
    
    tous_index = charger_tous_index("input")
    synonymes = charger_synonymes("input/origin_synonyms.json")
    products = charger_products("input/rearranged_products.jsonl")
    stopwords = charger_stopwords("data/stopwords_nltk.json")
    
    requetes_scores = [
        "chocolate italy",
        "cherry large", 
        "orange medium",
        "italy", 
        "cherry"
    ]
    
    for req in requetes_scores:
        print(f"\n '{req}'")
        tokens = traiter_requete(req, synonymes)
        tokens_essentiels = [t for t in tokens if t not in stopwords]
        
        docs_candidats = filtre_au_moins_un_token(tokens, tous_index, False)
        docs_finaux = filtre_tous_tokens_sauf_stopwords(tokens, docs_candidats, tous_index, stopwords, False)
        
        ranked = rank_documents(docs_finaux, tokens_essentiels, tous_index, products, top_k=3)
        
        print(f"   Tokens essentiels : {tokens_essentiels}")
        print(f"   {len(docs_candidats)} candidats -> {len(docs_finaux)} documents finaux")
        
        if ranked:
            print(f"   SCORES TOP 3 :")
            for i, (doc_url, score) in enumerate(ranked, 1):
                titre = products[doc_url].get('titre', 'N/A')[:60]
                print(f"     {i}. {score:6.2f} | {titre}")
        else:
            print("    AUCUN document ranké")


if __name__ == "__main__":
    etape1_jeu_requetes()
    etape2_scores_ranking()
