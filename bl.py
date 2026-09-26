import pandas as pd
import os

songs = pd.read_csv("songs.csv")

songs = songs.dropna(
    subset=["title", "artist", "bpm", "energy", "danceability", "valence"]
)


def get_songs(title, artist):
    result = songs[
        (songs["title"].str.lower().str.strip() == title.lower().strip()) &
        (songs["artist"].str.lower().str.strip() == artist.lower().strip())
    ]

    if not result.empty:
        return result.iloc[0]

    return None


title = input("Enter the title of the song: ")
artist = input("Enter the artist of the song: ")
result = get_songs(title, artist)

if result is None:
    print("Song not found.")

else:
    target = result

    recommendations = []

    bpm_min = songs["bpm"].min()
    bpm_max = songs["bpm"].max()

    energy_min = songs["energy"].min()
    energy_max = songs["energy"].max()

    dance_min = songs["danceability"].min()
    dance_max = songs["danceability"].max()

    valence_min = songs["valence"].min()
    valence_max = songs["valence"].max()

    target_bpm = (target["bpm"] - bpm_min) / (bpm_max - bpm_min)
    target_energy = (target["energy"] - energy_min) / (energy_max - energy_min)
    target_dance = (target["danceability"] - dance_min) / (dance_max - dance_min)
    target_valence = (target["valence"] - valence_min) / (valence_max - valence_min)

    for index, candidate in songs.iterrows():

        if(
            candidate["title"].lower().strip() == target["title"].lower().strip()
        and
            candidate["artist"].lower().strip() == target["artist"].lower().strip()
        ):
    
            continue

        candidate_bpm = (candidate["bpm"] - bpm_min) / (bpm_max - bpm_min)
        candidate_energy = (candidate["energy"] - energy_min) / (energy_max - energy_min)
        candidate_dance = (candidate["danceability"] - dance_min) / (dance_max - dance_min)
        candidate_valence = (candidate["valence"] - valence_min) / (valence_max - valence_min)
        difference = (abs(target_bpm - candidate_bpm)+ abs(target_energy - candidate_energy)+ abs(target_dance - candidate_dance)+abs(target_valence - candidate_valence))

        recommendations.append({
            "title": candidate["title"],
            "artist": candidate["artist"],
            "difference": difference
        })

    recommendations = pd.DataFrame(recommendations)
    recommendations = recommendations.drop_duplicates(
    subset=["title", "artist"]
)

    recommendations = recommendations.sort_values(
        "difference"
    ).reset_index(drop=True)

    top_3 = recommendations.head(3)

    print("\nRecommended Songs:")

    for index, song in top_3.iterrows():
        print(
            f"{index + 1}. {song['title']} - {song['artist']}"
            f"(difference: {song['difference']:.3f})"
        )