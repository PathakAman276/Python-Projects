# tasks
# scrape the top 100 songs 
# authenticate with spotify to create a new playlist 

from bs4 import BeautifulSoup
import lxml
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import clientinfo as ci


year = input("Enter the year : ")
month = input("Enter the month : ")
day = input("Enter the day : ")
date_string = f"{year}-{month}-{day}"
base_url = "https://www.billboard.com/charts/hot-100/"
full_url = f"{base_url}{date_string}/"

# using spotipy apk to authenticate that 
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com/",
        client_id=ci.client_id,
        client_secret=ci.client_info,
        show_dialog=True,
        cache_path="token.txt",
        username="aman", 
    )
)
user_id = sp.current_user()["id"]
song_uri = []

# I wasted one fucking hour just because mozzrilla want to feel a header up his ass i mean what is even the point of this shit anymore.
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}

# using request module to request api data 
responce = requests.get(full_url,headers=header)
soup = BeautifulSoup(responce.text, 'lxml')
# # this is another way i tried to do this but got stuck and wasted an hour in this shit 
# # then i got to know then the they were nested so here we are 
# numbers = soup.find_all(name="h3", id="title-of-a-story")
numbers = soup.select(selector="div div div div div div div div div div div ul li ul li h3")
list_of_songs = []

for song in numbers:
    # It took me 30 fucking minutes to strip the empty space from this text 
    list_of_songs.append((song.text).strip())
    result = sp.search(q=f"track:{(song.text).strip()} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uri.append(uri)
    except IndexError:
        print(f"{(song.text).strip()} does not exist in spotify skipped.")

# print(list_of_songs)
# print(song_uri)

# next targets 
# create a spotify playlist named yyyy-mm-dd Billboard 100 
# add songs one by one into the new playlist

playlist = sp.user_playlist_create(user=user_id,name=f"{date_string} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uri)

stopper = input("\n\nPlaylist Created Check Spotify \nPress ENTER to exit.")