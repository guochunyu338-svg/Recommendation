import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

songs = pd.read_csv("songs.csv")

songs = songs.dropna(
    subset=[
        "bpm",
        "energy",
        "danceability",
        "valence"
    ]
).reset_index(drop=True)

features = songs[
    ["bpm", "energy", "danceability", "valence"]
]

scaler = StandardScaler()

scaled_features = scaler.fit_transform(features)

kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

songs["cluster"] = kmeans.fit_predict(scaled_features)

title = input("Enter the title of the song: ")
artist = input("Enter the artist of the song: ")

result = songs[
    (songs["title"].str.lower().str.strip() == title.lower().strip()) &
    (songs["artist"].str.lower().str.strip() == artist.lower().strip())
]

if result.empty:
    print("Song not found.")

else:
    target = result.iloc[0]
    target_cluster = target["cluster"]
    target_index = target.name
    target_features = scaled_features[target_index]

    recommendations = songs[
    (songs["cluster"] == target_cluster) &
    ~(
        (songs["title"].str.lower().str.strip() == target["title"].lower().strip()) &
        (songs["artist"].str.lower().str.strip() == target["artist"].lower().strip())
    )
    ]
    recommendations = recommendations.drop_duplicates(
    subset=["title", "artist"]
)

    distances = []

    for index in recommendations.index:
       candidate_features = scaled_features[index]

       distance = (
           (target_features[0] - candidate_features[0]) ** 2
           + (target_features[1] - candidate_features[1]) ** 2
           + (target_features[2] - candidate_features[2]) ** 2
           + (target_features[3] - candidate_features[3]) ** 2
        ) ** 0.5

       distances.append(distance)

    recommendations["distance"] = distances
    recommendations = recommendations.sort_values(
    "distance"
    )
    print("\nRecommended Songs:")

top_3 = recommendations.head(3)

for rank, (index, song) in enumerate(top_3.iterrows(), start=1):
    print(
        f"{rank}. {song['title']} - {song['artist']}"
        f" (distance: {song['distance']:.3f})"
    )