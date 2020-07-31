import json
import requests


class CreatePlaylist:

    def __init__(self):
        with open('secrets.json') as secrets_file:
            secrets = json.load(secrets_file)
            self.spotify_token = secrets["spotify_token"]
            self.spotify_user_id = secrets["spotify_user_id"]

    def get_youtube_client(self):
        pass

    def get_liked_videos(self):
        pass

    # create spotify playlist
    def create_playlist(self):

        request_body = json.dumps({
            'name': 'Liked YT Vids',
            'description': 'All liked YT videos',
            'public': True
        })

        url = "https://api.spotify.com/v1/users/{}/playlists".format(
            self.spotify_user_id)

        response = requests.post(
            url,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )

        data = response.json()
        return data["id"]  # playlist id

    def get_spotify_uri(self, song_name, artist):

        url = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            song_name, artist)

        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )

        data = response.json()
        songs = data["tracks"]["items"]

        # first song that matches
        uri = songs[0]["uri"]
        return uri

    def add_song_to_playlist(self):
        pass
