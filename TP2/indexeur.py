import json
import os
from collections import defaultdict
from typing import Dict, List, Any


class Indexeur:
    def __init__(self, data_file: str = "products.jsonl", index_dir: str = "index"):
        self.data_file = data_file
        self.index_dir = index_dir
        self.index: Dict[str, List[Dict[str, Any]]] = defaultdict(list)  # terme -> postings
        self.docs: Dict[str, Dict[str, str]] = {}  # doc_id -> métadonnées

    # --- chargement données ---
    def charger_documents(self) -> List[Dict[str, Any]]:
        """Chaque ligne de data.json est un JSON avec au moins url, title, description."""
        with open(self.data_file, "r", encoding="utf-8") as f:
            lignes = f.readlines()
        docs = [json.loads(l) for l in lignes]
        return docs

    # --- normalisation ---
    def normaliser(self, texte: str) -> List[str]:
        """Tokenisation très simple : minuscule + split espaces."""
        if not texte:
            return []
        texte = texte.lower()
        # option simple : remplacer ponctuation de base par espace
        for c in ",.;:!?()[]{}\"'":
            texte = texte.replace(c, " ")
        tokens = [t for t in texte.split() if t]
        return tokens

    # --- construction index ---
    def indexer(self) -> None:
        docs = self.charger_documents()

        for i, doc in enumerate(docs):
            doc_id = f"doc_{i}"
            url = doc.get("url", "")
            title = doc.get("title", "")
            desc = doc.get("description", "")

            # enregistrer métadonnées document
            self.docs[doc_id] = {
                "url": url,
                "title": title,
                "description": desc,
            }

            # texte à indexer : titre + description (comme dans l’énoncé)
            texte = f"{title} {desc}"
            tokens = self.normaliser(texte)

            # dictionnaire local terme -> liste positions
            positions_par_terme: Dict[str, List[int]] = defaultdict(list)
            for pos, tok in enumerate(tokens):
                positions_par_terme[tok].append(pos)

            # remplir l’index inversé
            for terme, positions in positions_par_terme.items():
                self.index[terme].append(
                    {"doc_id": doc_id, "positions": positions}
                )

        self.sauvegarder_index()

    # --- sauvegarde ---
    def sauvegarder_index(self) -> None:
        os.makedirs(self.index_dir, exist_ok=True)

        # index inversé
        with open(os.path.join(self.index_dir, "index_inverse.json"), "w", encoding="utf-8") as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)

        # métadonnées documents
        with open(os.path.join(self.index_dir, "docs.json"), "w", encoding="utf-8") as f:
            json.dump(self.docs, f, ensure_ascii=False, indent=2)

        print(f"Index créé avec {len(self.index)} termes et {len(self.docs)} documents.")

if __name__ == "__main__":
    indexeur = Indexeur()
    indexeur.indexer()
