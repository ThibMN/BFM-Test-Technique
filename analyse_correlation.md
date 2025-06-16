# Analyse de la Corrélation entre Popularité et Streams Spotify

## Objectif
Ce script analyse la relation entre deux métriques importantes de Spotify :
- Le score de popularité Spotify (spotify-popularity)
- Le nombre de streams Spotify (spotify-streams)

## Méthodologie

### 1. Chargement et Préparation des Données
- Le script charge le fichier CSV contenant les données des 100 chansons
- Il gère les particularités du format (guillemets non fermés, JSON multilignes)
- Les données sont nettoyées et structurées dans un DataFrame pandas

### 2. Extraction des Séries Temporelles
- Pour chaque chanson, le script extrait les données de popularité et de streams
- Les données sont organisées avec les colonnes suivantes :
  - song_id
  - title
  - artist
  - date
  - spotify_streams
  - spotify_popularity

### 3. Analyse de la Corrélation
Le script effectue une analyse complète qui comprend :

#### a) Analyse Statistique
- Calcul du coefficient de corrélation de Pearson
- Calcul de la p-value pour évaluer la significativité statistique

#### b) Visualisations
Deux graphiques sont générés :

1. **Nuage de Points** (correlation_scatter.png)
   - Représente la relation directe entre popularité et streams
   - Permet de visualiser la distribution des données

2. **Évolution Temporelle** (correlation_evolution.png)
   - Montre l'évolution des moyennes de popularité et de streams dans le temps
   - Permet d'observer les tendances et les variations (pas spécialement affiché comme voulu malheureusement)

## Résultats
Les résultats sont sauvegardés sous forme de :
- Graphiques PNG dans le répertoire de travail
- Affichage dans la console du coefficient de corrélation et de sa p-value

## Utilisation
Pour exécuter l'analyse :
```python
python script1.py
```

## Notes Techniques
- Le script gère les cas particuliers comme les valeurs manquantes
- Les données sont converties en format numérique pour l'analyse
- Les visualisations sont optimisées pour la lisibilité 