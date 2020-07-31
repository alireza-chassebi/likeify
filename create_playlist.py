import json
import os

import requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


class CreatePlaylist:

    def __init__(self):
        with open('secrets.json') as secrets_file:
            secrets = json.load(secrets_file)
            self.spotify_token = secrets["spotify_token"]
            self.spotify_user_id = secrets["spotify_user_id"]
            self.youtube_client = self.get_youtube_client()

    def get_youtube_client(self):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()

        # from the Youtube DATA API
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube_client

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
