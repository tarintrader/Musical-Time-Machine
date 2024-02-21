import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
year = date.split("-")[0]

URL = f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(URL)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")

div_rows = soup.find_all(name="div", class_="o-chart-results-list-row-container")
h3_tags = [row.find(name="h3", id="title-of-a-story", class_="c-title") for row in div_rows]
tracklist = [tag.getText().strip() for tag in h3_tags]

CLIENT_ID = "273b1ae0fc9b41e1b40d521039bf92ae"
CLIENT_SECRET = "54ddf739278b44d28806059176b56aeb"
REDIRECT_URI = "http://example.com"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope="user-library-read playlist-modify-private"))

results = [sp.search(q=f"track: {track}"f"year: {year}") for track in tracklist]
tracklist_URIs = []
for result in results:
    try:
        tracklist_URIs.append(result["tracks"]["items"][0]["uri"])
    except:
        pass

user_id = sp.me()['id']

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=tracklist_URIs)
