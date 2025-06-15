# 1 - Analyse des données
### Structure actuelle des données (en champs):

- song_id : identifiant UUID unique
- title: titre de la musique
- artist: artiste de la musique (plusieurs si &)
- release_date: date de sortie de la musique au format iso
- image_url:  url de la couverture
- timeSeries: données JSON de l'évolution des métriques avec le temps (les métriques étant le nombre de streams et le score de popularité spotify)
- summaries: données JSON avec résumés et calculs d'évolution des métriques (en streams sur une période et score de popularité spotify)

### Problèmes de la structure:

- Si il y a plusieurs artistes ils sont stockés dans un seul champ (futur problème pour l'identification individuelle des artistes)
- Les données JSON sont assez compliqués à interpréter et requêter
- Les mêmes métriques apparaissent dans summaries et timeSeries ce qui prend de la place pour les mêmes données qui pourraient être uniformisées
- Ne prend pas d'autres platformes que spotify (j'ai l'impression)

### Proposition de modélisation PostgreSQL:

![[drawSQL-image-export-2025-06-15.png]]