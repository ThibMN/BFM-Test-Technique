import pandas as pd
import json
import matplotlib.pyplot as plt
import scipy.stats as stats

def load_data(file_path):
    """
    Charge un fichier CSV même mal formé (guillemets non fermés, champs JSON multilignes).
    Retourne un DataFrame pandas propre.
    """
    rows = []
    with open(file_path, encoding="utf-8") as f:
        # Lecture de l'en-tête pour récupérer les noms de colonnes
        header = f.readline().strip().split(",")
        expected_fields = len(header)
        buffer = ""
        # Lecture ligne par ligne pour reconstituer les lignes complètes (même si elles sont sur plusieurs lignes)
        for line in f:
            line = line.rstrip("\n")
            if not buffer:
                buffer = line
            else:
                buffer += "\n" + line
            # On considère qu'une ligne est complète si elle contient le bon nombre de virgules
            if buffer.count(",") >= expected_fields - 1:
                fields = []
                current = ""
                in_quotes = False
                # Découpage manuel pour gérer les virgules dans les champs entre guillemets
                for c in buffer:
                    if c == '"' and (not current or current[-1] != "\\"):
                        in_quotes = not in_quotes
                        current += c
                    elif c == "," and not in_quotes:
                        fields.append(current)
                        current = ""
                    else:
                        current += c
                fields.append(current)
                if len(fields) == expected_fields:
                    row = dict(zip(header, fields))
                    rows.append(row)
                buffer = ""
    df = pd.DataFrame(rows)
    # Nettoyage des noms de colonnes (suppression d'un éventuel index ou tabulation)
    df.columns = [c.strip().replace('1\t', '') for c in df.columns]
    print(df.columns)
    # Correction du nom de la première colonne si besoin
    if df.columns[0].endswith('song_id'):
        df = df.rename(columns={df.columns[0]: 'song_id'})
    # Si la première colonne n'est pas pertinente, on la retire
    if df.columns[0] not in ('song_id', 'title', 'artist'):
        df = df.drop(df.columns[0], axis=1)
    # On garde uniquement les lignes avec un song_id et un timeSeries non vide
    df = df[df['song_id'].notna() & df['timeSeries'].notna()]
    return df

def extract_timeseries(df):
    """
    Extrait les valeurs 'spotify-popularity' et 'spotify-streams' du champ timeSeries.
    Retourne un DataFrame avec song_id, title, artist, date, spotify_streams, spotify_popularity.
    """
    import re
    records = []
    for _, row in df.iterrows():
        try:
            # Nettoyage du champ timeSeries pour obtenir un JSON valide
            ts_str = row['timeSeries']
            # Suppression des guillemets extérieurs si présents
            if ts_str.startswith('"') and ts_str.endswith('"'):
                ts_str = ts_str[1:-1]
            # Remplacement des doubles guillemets par des simples
            ts_str = ts_str.replace('""', '"')
            # Correction des éventuels caractères d'échappement
            ts_str = re.sub(r'\\(.)', r'\1', ts_str)
            # Conversion en objet Python
            ts = json.loads(ts_str)
            for entry in ts:
                # On ne garde que les entrées qui ont à la fois popularity et streams
                if ('spotify-popularity' in entry) and ('spotify-streams' in entry):
                    records.append({
                        'song_id': row['song_id'],
                        'title': row['title'],
                        'artist': row['artist'],
                        'date': entry.get('date'),
                        'spotify_streams': entry.get('spotify-streams'),
                        'spotify_popularity': entry.get('spotify-popularity')
                    })
        except Exception as e:
            print(f"Erreur parsing timeSeries pour {row.get('title', '')}: {e}")
    print(f"{len(records)} lignes extraites pour l'analyse.")
    return pd.DataFrame(records)

def analyse_correlation(df):
    """
    Affiche la corrélation entre la popularité Spotify et les streams Spotify dans le temps.
    Génère deux graphiques enregistrés en PNG.
    """
    # Vérification de la présence des colonnes nécessaires
    if df.empty or 'spotify_popularity' not in df.columns or 'spotify_streams' not in df.columns:
        print("Aucune donnée exploitable pour l'analyse.")
        return

    # Suppression des lignes avec des valeurs manquantes
    df = df.dropna(subset=['spotify_popularity', 'spotify_streams'])
    if df.empty:
        print("Aucune donnée après suppression des valeurs manquantes.")
        return

    # Conversion des colonnes en numériques
    df['spotify_popularity'] = pd.to_numeric(df['spotify_popularity'])
    df['spotify_streams'] = pd.to_numeric(df['spotify_streams'])

    # Calcul de la corrélation de Pearson
    corr, pval = stats.pearsonr(df['spotify_popularity'], df['spotify_streams'])
    print(f"Corrélation (Pearson) : {corr:.2f} (p-value={pval:.4f})")

    # Premier graphique : nuage de points
    plt.figure(figsize=(8,5))
    plt.scatter(df['spotify_popularity'], df['spotify_streams'], alpha=0.5)
    plt.xlabel('Spotify Streams')
    plt.ylabel('Spotify Popularity')
    plt.title('Corrélation entre Spotify Popularity et Spotify Streams')
    plt.savefig("correlation_scatter.png")
    plt.close()

    # Deuxième graphique : évolution temporelle des moyennes
    df_grouped = df.groupby('date')[['spotify_streams', 'spotify_popularity']].mean().reset_index()
    plt.figure(figsize=(24,10))
    plt.plot(df_grouped['date'], df_grouped['spotify_streams'], label='Spotify Streams (moyenne)')
    plt.plot(df_grouped['date'], df_grouped['spotify_popularity'], label='Spotify Popularity (moyenne)')
    plt.xlabel('Date')
    plt.ylabel('Valeur')
    plt.title('Évolution temporelle (moyenne sur toutes les chansons)')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("correlation_evolution.png")
    plt.close()

def main():
    # Chargement des données depuis le CSV
    df = load_data("../100-songs-audience-report.csv")
    if df is None:
        return

    # Extraction des séries temporelles à partir du champ JSON
    timeseries_df = extract_timeseries(df)

    # Analyse de la corrélation et génération des graphiques
    analyse_correlation(timeseries_df)

if __name__ == "__main__":
    main()