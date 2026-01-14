# README - TP3

## Analyse de la performance du ranking

 ### Premières observations

Dans un premier temps, voici les poids qui ont été fixés:
* Titre: 2.0 <- signal prioritaire
* Description: 1.0 <- poids standard
* Reviews: 0.5 <- poids faible

Après observation des sorties obtenues, voici ce que l'on peut noter:

**Forces**
* Filtrage efficace: -85% des documents candidats
* Ranking simple et fonctionnel pour la plupart des cas

**Problèmes identifiés**
* pour "italy", on obtient des scores BM25 nuls: c'est probablement lié au fait que "italy" n'apparaît pas dans les titres et que le champ des origines n'a pas encore été pris en compte dans le score
* on observe des scores identiques pour "chocolate italy" car les documents sont très similaires, ce qui conduit naturellement à des scores proches

Il faudrait donc tester d'autres combinaisons de poids et éventuellement ajouter le champ _origine_ pour des requêtes de type pays.


### Ajustements

#### Ajout du signal _origine_
En ajoutant le signal _origine_ avec un poids à 1.0, on remarque que les scores pour 'italy' ne sont plus nuls mais les résultats obtenus ne sont pas très pertinents:
```
 'italy'
   Tokens essentiels : ['italy']
   21 candidats -> 21 documents finaux
   SCORES TOP 3 :
     1.   1.99 | Kids' Light-Up Sneakers - Red 6
     2.   1.99 | Classic Leather Sneakers - Black42
     3.   1.99 | Dark Red Energy Potion - Six pack
```
Il faudrait donc augmenter le poids correspondant. En l'augmentant à 5.0, on remarque que les résultats sont déjà plus pertinents:
```
 'italy'
   Tokens essentiels : ['italy']
   21 candidats -> 21 documents finaux
   SCORES TOP 3 :
     1.   9.94 | Classic Leather Sneakers - White41
     2.   9.94 | web-scraping.dev product page 2
     3.   9.94 | Classic Leather Sneakers - Black41
```


#### Equilibrage des signaux
Afin d'équilibrer les signaux, voici les poids fixés:
* Titre: 4.0
* Description: 1.0
* Reviews: 0.5
* Origine: 5.0

En observant les résultats pour "italy", on remarque la présence de "Dark Red Energy Potion":
```
 'italy'
   Tokens essentiels : ['italy']
   21 candidats -> 21 documents finaux
   SCORES TOP 3 :
     1.   9.94 | Classic Leather Sneakers - Black40
     2.   9.94 | Dark Red Energy Potion - Six pack
     3.   9.94 | Classic Leather Sneakers - White41
```
Je décide donc d'augmenter d'une unité le poids de l'origine et on observe que les résultats obtenus sont plus pertinents:
```
  'italy'
   Tokens essentiels : ['italy']
   21 candidats -> 21 documents finaux
   SCORES TOP 3 :
     1.  11.93 | Classic Leather Sneakers
     2.  11.93 | Classic Leather Sneakers - Black40
     3.  11.93 | Box of Chocolate Candy - Cherry medium
```
Cependant, on remarque que les scores sont identiques et c'est également le cas pour autres requêtes. Je décide alors d'ajouter une autre composante au score: une sorte de tie-breaker. 


#### Ajout du tie-breaker
Le tie-breaker prend en compte 
* la position du premier token dans le titre: si le token est en début de titre, le score est boosté
* la longueur du titre: on privilégie les titres concis car plus descriptifs.

Voici les résulats obtenus pour 'italy' après l'ajout du tie-breaker:
```
 'italy'
   Tokens essentiels : ['italy']
   21 candidats -> 21 documents finaux
   SCORES TOP 3 :
     1.  11.96 | Classic Leather Sneakers
     2.  11.96 | Classic Leather Sneakers
     3.  11.95 | Kids' Light-Up Sneakers - Red 6
```
Il reste quelques doublons persistants mais de manière générale, les résultats observés sont plutôt satisfaisants. 



