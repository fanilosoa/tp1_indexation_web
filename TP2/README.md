# README

## Structure des Index

Voici les différents formats des index.
### Format - index des titres
```python
{
    "titre1": [
        "lien_1",
        "lien_2",
        "lien_3"
    ],
    "titre2": [
        "lien_1",
        "lien_2",
        "lien_3",
        "lien_4
    ]

}
```

### Format - index des reviews
```python
{
  "id_doc0": {
    "nb_reviews": 0,
    "avg_rating": 0.0,
    "last_rating": 0
  },
  "id_doc1": {
    "nb_reviews": 5,
    "avg_rating": 4.6,
    "last_rating": 4
  }
}
```

### Format - index des features (ex: brand)
```python
{
    "marque_1": [
        "doc_1",
        "doc_24",
        "doc_25",
        "doc_26"
    ],
    "marque_2": [
        "doc_8",
        "doc_9",
        "doc_10",
        "doc_11",
        "doc_12"
    ]

}
```
En plus des features "brand" et "origin", la feature "material" a été extraite. Parmi les matériaux observés, il y a eu "leather", "high-quality" ou encore "breathable". On peut également remarquer la présence surprenante du matériau "chocolate". 


### Format - index des positions (ex: titres)
```python
{
  "titre1": [
    {
      "doc_id": "doc_0",
      "positions": [
        0
      ]
    },
    {
      "doc_id": "doc_133",
      "positions": [
        0
      ]
    },
  ],
  "titre2": [
    {
      "doc_id": "doc_0",
      "positions": [
        1, 5
      ]
    },
    {
      "doc_id": "doc_133",
      "positions": [
        1, 5
      ]
    },
  ]
}
```
La sortie s'interprète de la manière suivante: le titre 2 apparaît dans le document doc_0 aux positions 1 et 5. 

On remarque dans les sorties obtenues que les positions sont généralement les mêmes pour chaque titre car il y a des documents dupliqués dans la base de données.


## Choix techniques

### Tokenisation
Deux techniques de tokenisation ont été utilisées:
* split() pour les features et les reviews car il s'agit généralement de textes courts avec des structures simples
* NLTK pour les titres et les descriptions car les phrases sont plus complexes.

### Normalisation
La normalisation permet d'unifier les variantes en les transformant dans un format plus simple. Voici les pratiques appliquées pour cette étape:
* on garde uniquement les mots d'une longueur supérieure à 2 pour éviter de trop polluer l'index
* tous les mots sont mis entièrement en minuscules pour uniformiser la casse
* les signes de ponctuation sont retirés
* utilisation de NLTK dans certains cas: permet de gérer la tokensiation, le stemming, la lemmatisation et les stopwords.






