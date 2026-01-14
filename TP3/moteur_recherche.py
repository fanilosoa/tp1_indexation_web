from index_utils import charger_tous_index, charger_synonymes, charger_products, charger_stopwords
from filtre import traiter_requete, filtre_au_moins_un_token, filtre_tous_tokens_sauf_stopwords
from ranking import rank_documents

def rechercher(requete, top_k=10):
    tous_index = charger_tous_index("input")
    synonymes = charger_synonymes("input/origin_synonyms.json")
    products = charger_products("input/rearranged_products.jsonl")
    stopwords = charger_stopwords("data/stopwords_nltk.json")

    tokens = traiter_requete(requete, synonymes)
    tokens_essentiels = [t for t in tokens if t not in stopwords]

    docs_candidats = filtre_au_moins_un_token(tokens, tous_index)
    docs_finaux = filtre_tous_tokens_sauf_stopwords(tokens, docs_candidats, tous_index, stopwords)

    ranked = rank_documents(docs_finaux, tokens_essentiels, tous_index, products, top_k=top_k)
    return ranked

def tester_partie3():
    print("=== TEST PARTIE 3 ===")

    print("\n1 Chargement des données...")
    tous_index = charger_tous_index("input")
    synonymes = charger_synonymes("input/origin_synonyms.json")
    products = charger_products("input/rearranged_products.jsonl")
    stopwords = charger_stopwords("data/stopwords_nltk.json")

    requetes_test = [
        "chocolate italy",
        "cherry large",
        "orange medium",
        "italy",
        "cherry"
    ]

    print("\n TESTS RANKING (Top 3 pour chaque requête)")
    for i, requete in enumerate(requetes_test, 1):
        print(f"\n {i}. '{requete}'")

        tokens = traiter_requete(requete, synonymes)
        tokens_essentiels = [t for t in tokens if t not in stopwords]

        docs_candidats = filtre_au_moins_un_token(tokens, tous_index)
        docs_finaux = filtre_tous_tokens_sauf_stopwords(tokens, docs_candidats, tous_index, stopwords)

        ranked = rank_documents(docs_finaux, tokens_essentiels, tous_index, products, top_k = 3)

        print(f"   -> {len(tokens)} tokens -> {len(docs_candidats)} cand. -> {len(docs_finaux)} finaux")
        print(f"   -> Top 3:")
        for j, (doc_url, score) in enumerate(ranked, 1):
            titre = products[doc_url].get('titre', 'N/A')[:50] + "..."
            print(f"        {j}. {score:.2f} | {titre}")
    
    print("\n Ranking terminé ")
    return True

if __name__ == "__main__":
    tester_partie3()