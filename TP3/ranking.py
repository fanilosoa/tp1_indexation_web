import math
import json
from index_utils import normaliser_feature, charger_products

# Calcul du score BM25
def bm25_term_score(tf, df, N, doc_len, avg_doc_len, k1=1.2, b=0.75):
    """
    Score BM25 pour un token dans un document.
    tf : fréquence d'apparition du token dans le document
    df : nombre de documents contenant le token
    N  : nombre total de documents
    """
    if tf == 0 or df == 0:
        return 0.0
    idf = math.log((N - df + 0.5) / (df + 0.5) + 1)
    norm_tf = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_len / avg_doc_len)))
    return idf * norm_tf

# Fréquence d'apparition d'un token
def term_freq_in_text(token, text):
    """Compte combien de fois token apparaît dans text normalisé."""
    tokens = normaliser_feature(text)
    return tokens.count(token), len(tokens)

# Score BM25 du titre + description
def bm25_document_score(doc_url, tokens_essentiels, tous_index, products):
    """
    Combine BM25 titre + description pour un document et une requête.
    """
    doc = products[doc_url]
    titre = doc.get("titre", "")
    desc = doc.get("description", "")
    features = doc.get("features", {})
    origine = features.get("made in", "")

    # On suppose N = nombre de documents
    N = len(products)

    score = 0.0

    for t in tokens_essentiels:
        # Titre
        tf_title, len_title = term_freq_in_text(t, titre)
        df_title = len(tous_index["title"].get(t, []))
        avg_len_title = 1 + sum(
            len(normaliser_feature(products[u].get("titre", "")))
            for u in products
        ) / max(N, 1)
        score += 4.0 * bm25_term_score(tf_title, df_title, N, len_title or 1, avg_len_title)

        # Description
        tf_desc, len_desc = term_freq_in_text(t, desc)
        df_desc = len(tous_index["description"].get(t, []))
        avg_len_desc = 1 + sum(
            len(normaliser_feature(products[u].get("description", "")))
            for u in products
        ) / max(N, 1)
        score += 1.0 * bm25_term_score(tf_desc, df_desc, N, len_desc or 1, avg_len_desc)

        # Origine
        tf_origin, len_origin = term_freq_in_text(t, origine)
        df_origine = len(tous_index["origin"].get(t, []))
        avg_len_origine = 1 + sum(
            len(normaliser_feature(products[u].get("product_features", {}).get("made in", "")))
            for u in products
        ) / max(N, 1)
        score += 6.0 * bm25_term_score(tf_origin, df_origine, N, len_origin or 1, avg_len_origine)


    return score

# Fonction de match exact
def exact_match_bonus(doc_url, tokens_essentiels, products):
    """
    Bonus si le titre contient (presque) tous les tokens essentiels.
    """
    titre_tokens = set(normaliser_feature(products[doc_url].get("titre", "")))
    if all(t in titre_tokens for t in tokens_essentiels):
        return 2.0  # gros bonus
    if any(t in titre_tokens for t in tokens_essentiels):
        return 0.5  # petit bonus
    return 0.0

# Prise en compte des avis
def reviews_score(doc_url, products):
    """
    Signal simple basé sur les avis.
    Ajuste selon ce que tu as dans rearranged_products.jsonl.
    """
    reviews = products[doc_url].get("reviews", [])
    if not reviews:
        return 0.0
    n_reviews = len(reviews)
    return math.log(1 + n_reviews)

# Ajout d'un tie-breaker
def tie_breaker_bonus(doc_url, tokens_essentiels, products):
    doc = products[doc_url]
    titre_tokens = normaliser_feature(doc["titre"])
    
    # Position 1er token
    for i, token in enumerate(titre_tokens):
        if token in tokens_essentiels:
            return 0.2 / (i + 1)
    return 0.1 / max(len(titre_tokens), 1)



# Calcul du score global
def score_document(doc_url, tokens_essentiels, tous_index, products):
    """
    Score global combinant :
      - BM25 titre + description
      - match exact / couverture dans le titre
      - signal reviews
      - tie-breaker
    """
    score = 0.0
    score += bm25_document_score(doc_url, tokens_essentiels, tous_index, products)
    score += exact_match_bonus(doc_url, tokens_essentiels, products)
    score += 0.5 * reviews_score(doc_url, products)
    score += tie_breaker_bonus(doc_url, tokens_essentiels, products)

    return score

# Classement des documents
def rank_documents(docs_finaux, tokens_essentiels, tous_index, products, top_k=10):
    """
    Retourne les documents finaux triés par score décroissant.
    """
    scored = [
        (doc_url, score_document(doc_url, tokens_essentiels, tous_index, products))
        for doc_url in docs_finaux
    ]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]

def rank_documents_json(docs_finaux, tokens_essentiels, tous_index, products, top_k=10):
    """
    Ranking + formatage JSON pour le livrable
    """

    scored = [
        (doc_url, score_document(doc_url, tokens_essentiels, tous_index, products))
        for doc_url in docs_finaux
    ]
    scored.sort(key=lambda x: x[1], reverse=True)
    top_docs = scored[:top_k]
    
    # Construction résultats JSON
    resultats = {
        "metadata": {
            "requete": " ".join(tokens_essentiels),
            "tokens_essentiels": tokens_essentiels,
            "nombre_total_documents": len(products),
            "documents_candidats": len(docs_finaux),
            "documents_finaux": len(docs_finaux),
            "documents_retournes": len(top_docs),
            "top_k": top_k,
            "poids_config": {
                "titre": 4.0,
                "description": 1.0,
                "origin": 5.0,
                "reviews": 0.5
            }
        },
        "documents": []
    }
    
    # Formatage chaque document
    for i, (doc_url, score) in enumerate(top_docs, 1):
        doc = products[doc_url]
        resultats["documents"].append({
            "rang": i,
            "titre": doc.get("titre", ""),
            "url": doc_url,
            "description": doc.get("description", ""),
            "score_ranking": round(float(score), 2),
            "origine": doc.get("features", {}).get("made in", ""),
            "reviews": len(doc.get("reviews", [])),
            "score_breakdown": {
                "bm25": round(float(score - tie_breaker_bonus(doc_url, tokens_essentiels, products) - 0.5 * reviews_score(doc_url, products)), 2),
                "exact_match": round(float(exact_match_bonus(doc_url, tokens_essentiels, products)), 2),
                "reviews": round(float(0.5 * reviews_score(doc_url, products)), 2),
                "tie_breaker": round(float(tie_breaker_bonus(doc_url, tokens_essentiels, products)), 2)
            }
        })
    
    return resultats
