import json
import os
from collections import defaultdict

def charger_documents(data_file="products.jsonl"):
    """Charge products.jsonl"""
    with open(data_file, "r", encoding="utf-8") as f:
        lignes = f.readlines()
    return [json.loads(l) for l in lignes if l.strip()]

def normaliser_feature(valeur):
    """Nettoie valeurs features"""
    if not valeur or not isinstance(valeur, str):
        return []
    
    valeur = str(valeur).lower()
    for c in ",.;:!?()[]{}\"'":
        valeur = valeur.replace(c, " ")
    
    tokens = [t.strip() for t in valeur.split() if len(t.strip()) > 2]
    return tokens

def indexer_features():
    """Crée index_origin.json et index_brand.json"""
    docs = charger_documents()
    origin_index = defaultdict(list) 
    brand_index = defaultdict(list)
    material_index = defaultdict(list) 
    
    for i, doc in enumerate(docs):
        doc_id = f"doc_{i}"
        features = doc.get('product_features', {})
        
        # BRAND_INDEX
        brand = features.get('brand', '')
        brand_tokens = normaliser_feature(brand)
        for token in brand_tokens:
            if doc_id not in brand_index[token]:
                brand_index[token].append(doc_id)
        
        # ORIGIN_INDEX (made in)
        origin_keys = ['made in']
        origin_value = ''
        for key in origin_keys:
            if key in features:
                origin_value = features[key]
                break
        
        origin_tokens = normaliser_feature(origin_value)
        for token in origin_tokens:
            if doc_id not in origin_index[token]:
                origin_index[token].append(doc_id)
        
        # MATERIAL_INDEX
        material = features.get('material', '')
        material_tokens = normaliser_feature(material)
        for token in material_tokens:
            if doc_id not in material_index[token]:
                material_index[token].append(doc_id)
    
    # Sauvegarde 3 fichiers distincts
    os.makedirs("index", exist_ok=True)
    
    with open("index/index_brand.json", "w", encoding="utf-8") as f:
        json.dump(dict(brand_index), f, ensure_ascii=False, indent=2)
    
    with open("index/index_origine.json", "w", encoding="utf-8") as f:
        json.dump(dict(origin_index), f, ensure_ascii=False, indent=2)
    
    with open("index/index_material.json", "w", encoding="utf-8") as f:
        json.dump(dict(material_index), f, ensure_ascii=False, indent=2)
    
    # Stats
    print(f"Index Features créé :")
    print(f"- BRAND_INDEX : {len(brand_index)} marques -> {sum(len(docs) for docs in brand_index.values())} docs")
    print(f"- ORIGIN_INDEX: {len(origin_index)} origines -> {sum(len(docs) for docs in origin_index.values())} docs")
    print(f"- MATERIAL_INDEX: {len(material_index)} matériaux -> {sum(len(docs) for docs in material_index.values())} docs")
    
    print(f"\n--- Top 5 BRANDS ---")
    for brand, doc_ids in sorted(brand_index.items(), key=lambda x: len(x[1]), reverse=True)[:5]:
        print(f"   '{brand}' -> {len(doc_ids)} docs")
    
    print(f"\n---Top 5 ORIGINS ---")
    for origin, doc_ids in sorted(origin_index.items(), key=lambda x: len(x[1]), reverse=True)[:5]:
        print(f"   '{origin}' -> {len(doc_ids)} docs")
    
    print(f"\n---Top 5 MATERIALS ---")
    for origin, doc_ids in sorted(material_index.items(), key=lambda x: len(x[1]), reverse=True)[:5]:
        print(f"   '{origin}' -> {len(doc_ids)} docs")

if __name__ == "__main__":
    indexer_features()
