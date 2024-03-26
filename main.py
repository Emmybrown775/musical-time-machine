import os

from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

scope = "user-library-read playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ["CLIENT_ID"],
                                               client_secret=os.environ["CLIENT_SECRET"],
                                               redirect_uri="http://example.com",
                                               scope=scope,

                                               ))

user_id = sp.current_user()["id"]

travel_date = input("What year do you want to travel to? Type the date in this format YYYY-MM-DD:")
year = travel_date[:4]
url = f"https://www.billboard.com/charts/hot-100/{travel_date}"

response = requests.get(url)
data = response.text

soup = BeautifulSoup(data, "html.parser")

song_titles = [title.find(name="h3").get_text().strip() for title in
               soup.find_all(name="div", class_="o-chart-results-list-row-container")]

song_links = []
for song in song_titles:
    response = sp.search(q=f"track:{song} year:{year}", type="track")

    try:
        song_link = response["tracks"]["items"][0]["uri"]
        song_links.append(song_link)
        print(song_link)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

create_playlist = sp.user_playlist_create(user=user_id, name=f"{travel_date} Billboard 100")
print(create_playlist)
playlist_id = create_playlist["id"]

add_to_playlists = sp.playlist_add_items(playlist_id=playlist_id, items=song_links)
print(add_to_playlists)
