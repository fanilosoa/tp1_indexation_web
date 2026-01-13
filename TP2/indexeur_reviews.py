import json
import os
from statistics import mean

def charger_documents(data_file="products.jsonl"):
    """Charge products.jsonl"""
    with open(data_file, "r", encoding="utf-8") as f:
        lignes = f.readlines()
    return [json.loads(l) for l in lignes if l.strip()]

def extraire_reviews(doc):
    """Extrait reviews avec rating"""
    reviews = doc.get('product_reviews', [])
    return [r for r in reviews if 'rating' in r]

def calculer_stats_reviews(reviews):
    """nb_reviews, avg_rating, last_rating"""
    if not reviews:
        return {'nb_reviews': 0, 'avg_rating': 0.0, 'last_rating': 0}
    
    ratings = [r['rating'] for r in reviews]
    
    # Dernière note : date la plus récente
    last_review = max(reviews, key=lambda r: r.get('date', ''))
    last_rating = last_review['rating']
    
    return {
        'nb_reviews': len(reviews),
        'avg_rating': round(mean(ratings), 2),
        'last_rating': last_rating
    }

def indexer_reviews():
    """Crée index_reviews.json"""
    docs = charger_documents()
    index_reviews = {}
    
    for i, doc in enumerate(docs):
        doc_id = f"doc_{i}"
        reviews = extraire_reviews(doc)
        index_reviews[doc_id] = calculer_stats_reviews(reviews)
    
    # Sauvegarde
    os.makedirs("index", exist_ok=True)
    
    with open("index/index_reviews.json", "w", encoding="utf-8") as f:
        json.dump(index_reviews, f, ensure_ascii=False, indent=2)
    
    # Stats globales
    total_reviews = sum(d['nb_reviews'] for d in index_reviews.values())
    docs_avec_reviews = sum(1 for d in index_reviews.values() if d['nb_reviews'] > 0)
    
    print(f"Index Reviews : {len(index_reviews)} docs, {total_reviews} reviews, {docs_avec_reviews} docs avec reviews")

if __name__ == "__main__":
    indexer_reviews()
