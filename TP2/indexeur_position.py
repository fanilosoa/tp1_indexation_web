import json
import os
from collections import defaultdict
import nltk
from nltk.corpus import stopwords

# NLTK stopwords
STOPWORDS = set(stopwords.words('english'))

def normaliser_position_nltk(texte):
    """NLTK tokenisation NUMÉROTÉE avec positions"""
    if not texte:
        return []
    
    # Minuscules + nettoyage ponctuation
    texte = texte.lower()
    for c in ",.;:!?()[]{}\"'":
        texte = texte.replace(c, " ")
    
    # NLTK tokenisation
    tokens = nltk.word_tokenize(texte)
    
    # Filtre : alpha + >2 lettres + pas stopwords
    tokens_filtres = [t for t in tokens if t.isalpha() and len(t) > 2 and t not in STOPWORDS]
    return tokens_filtres

def charger_documents(data_file="products.jsonl"):
    with open(data_file, "r", encoding="utf-8") as f:
        lignes = f.readlines()
    return [json.loads(l) for l in lignes if l.strip()]

def indexer_positions():
    """Crée index_positions_titre.json + index_positions_description.json (NLTK)"""
    docs = charger_documents()
    
    index_pos_titre = defaultdict(list)
    index_pos_description = defaultdict(list)
    
    for i, doc in enumerate(docs):
        doc_id = f"doc_{i}"
        title = doc.get("title", "")
        description = doc.get("description", "")
        
        # POSITIONS TITRE (NLTK)
        title_tokens = normaliser_position_nltk(title)
        positions_titre = defaultdict(list)
        for pos, token in enumerate(title_tokens):
            positions_titre[token].append(pos)
        
        for token, positions in positions_titre.items():
            index_pos_titre[token].append({
                "doc_id": doc_id,
                "positions": positions
            })
        
        # POSITIONS DESCRIPTION (NLTK)
        desc_tokens = normaliser_position_nltk(description)
        positions_desc = defaultdict(list)
        for pos, token in enumerate(desc_tokens):
            positions_desc[token].append(pos)
        
        for token, positions in positions_desc.items():
            index_pos_description[token].append({
                "doc_id": doc_id,
                "positions": positions
            })
    
    # Sauvegarde
    os.makedirs("index", exist_ok=True)
    
    with open("index/index_positions_titre.json", "w", encoding="utf-8") as f:
        json.dump(dict(index_pos_titre), f, ensure_ascii=False, indent=2)
    
    with open("index/index_positions_description.json", "w", encoding="utf-8") as f:
        json.dump(dict(index_pos_description), f, ensure_ascii=False, indent=2)
    
    # Stats
    print(f"Index Positions NLTK créé :")
    print(f"- {len(index_pos_titre)} termes titre (avec positions)")
    print(f"- {len(index_pos_description)} termes description (avec positions)")
    
    # Exemple concret
    if index_pos_titre:
        exemple_token = list(index_pos_titre.keys())[0]
        print(f"\n Exemple '{exemple_token}':")
        for posting in index_pos_titre[exemple_token][:2]:
            print(f"   {posting['doc_id']}: positions {posting['positions']}")

if __name__ == "__main__":
    indexer_positions()
