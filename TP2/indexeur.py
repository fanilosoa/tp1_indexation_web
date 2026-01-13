import json
import os
from collections import defaultdict
import nltk
from nltk.corpus import stopwords

# NLTK stopwords anglais
STOPWORDS = set(stopwords.words('english'))

def normaliser(texte):
    """NLTK tokenisation + stopwords"""
    if not texte:
        return []
    
    # Minuscules + ponctuation
    texte = texte.lower()
    for c in ",.;:!?()[]{}\"'":
        texte = texte.replace(c, " ")
    
    # NLTK tokenisation
    tokens = nltk.word_tokenize(texte)
    
    # Filtre : alpha + >2 lettres + pas stopwords
    return [t for t in tokens if t.isalpha() and len(t) > 2 and t not in STOPWORDS]

def charger_documents(data_file="products.jsonl"):
    """Charge products.jsonl"""
    with open(data_file, "r", encoding="utf-8") as f:
        lignes = f.readlines()
    return [json.loads(l) for l in lignes if l.strip()]

def indexer():
    """Crée index_titre.json + index_description.json"""
    docs = charger_documents()
    index_titre = defaultdict(list)
    index_description = defaultdict(list)
    
    for doc in docs:
        url = doc.get("url", "")
        
        # Index titre
        tokens_titre = normaliser(doc.get("title", ""))
        for token in tokens_titre:
            if url not in index_titre[token]:
                index_titre[token].append(url)
        
        # Index description
        tokens_desc = normaliser(doc.get("description", ""))
        for token in tokens_desc:
            if url not in index_description[token]:
                index_description[token].append(url)
    
    # Sauvegarde
    os.makedirs("index", exist_ok=True)
    
    with open("index/index_titre.json", "w", encoding="utf-8") as f:
        json.dump(dict(index_titre), f, ensure_ascii=False, indent=2)
    
    with open("index/index_description.json", "w", encoding="utf-8") as f:
        json.dump(dict(index_description), f, ensure_ascii=False, indent=2)
    
    nb_docs = len(docs)
    print(f"Index NLTK créé : {len(index_titre)} termes titre, {len(index_description)} termes description, {nb_docs} docs")

if __name__ == "__main__":
    indexer()
