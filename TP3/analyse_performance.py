import json
from index_utils import charger_tous_index, charger_synonymes, charger_products, charger_stopwords
from filtre import traiter_requete, filtre_au_moins_un_token, filtre_tous_tokens_sauf_stopwords
from ranking import rank_documents, rank_documents_json, normaliser_feature


JEUX_REQUETES = {
    "simples": ["italy", "chocolate", "cherry", "orange"],
    "multi": ["chocolate italy", "cherry large", "orange medium"],
    "synonymes": ["fr", "usa", "it"]
}

def analyser_requete_json(requete, docs_finaux, tous_index, products):
    """Test une requête + affiche JSON"""
    tokens = normaliser_feature(requete)
    resultats = rank_documents_json(docs_finaux, tokens, tous_index, products, top_k=3)
    
    print(f"\n '{requete}' -> JSON :")
    print(json.dumps(resultats, indent=2, ensure_ascii=False)[:1000] + "...")
    
    return resultats

# Fonction pour sauvegarder
def sauvegarder_resultats_json(resultats, nom_fichier="resultats_ranking.json"):
    """Sauvegarde résultats formatés en JSON"""
    with open(f"output/{nom_fichier}", "w", encoding="utf-8") as f:
        json.dump(resultats, f, indent=2, ensure_ascii=False)
    print(f" Résultats sauvegardés : {nom_fichier}")

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

    all_results = {}
    
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

        resultats_json = analyser_requete_json(req, docs_finaux, tous_index, products)
        all_results[req] = resultats_json
        sauvegarder_resultats_json(resultats_json, f"resultats_{req.replace(' ', '_')}.json")
    
    sauvegarder_resultats_json({"requetes": all_results}, "resultats_complets_tp3.json")


if __name__ == "__main__":
    etape1_jeu_requetes()
    etape2_scores_ranking()
