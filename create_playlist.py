import json
import os

import requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl


spotify_token_instructions = "\n1. Visit the URL below \n2. Click GET TOKEN followed by REQUEST TOKEN \n3. LOGIN if required, if not go to step 4\n4. Copy and enter OAuth token below 😀 \nURL:{}\nEnter here:".format(
    "https://developer.spotify.com/console/post-playlist-tracks/?playlist_id=&position=&uris=")

spotify_id_instructions = "\n1. Visit the URL below \n2. LOGIN if required, if not go to step 3 \n3. Copy and enter Username below 😀 \nURL:{}\nEnter here:".format(
    'https://www.spotify.com/us/account/overview/?utm_source=play&utm_campaign=wwwredirect')


class CreatePlaylist:

    def __init__(self, youtube_client):
        self.youtube_client = youtube_client

        self.spotify_token = self.getSpotifyInfo(spotify_token_instructions)

        self.spotify_user_id = self.getSpotifyInfo(spotify_id_instructions)

        self.all_song_info = {}

    def get_liked_videos(self):
        request = self.youtube_client.videos().list(
            part="snippet,contentDetails,statistics",
            myRating="like"
        )
        response = request.execute()

        for item in response["items"]:
            video_title = item["snippet"]["title"]
            youtube_url = "https://www.youtube.com/watch?v={}".format(
                item["id"])
            # extract video information
            video = youtube_dl.YoutubeDL({}).extract_info(
                youtube_url, download=False
            )
            # "track" and "artist" attributes are available for the media that is a track or a part of a music album
            song_name = video["track"]
            artist = video["artist"]

            # skip all videos that are not songs
            if song_name is not None and artist is not None:
                spotify_uri = self.get_spotify_uri(song_name, artist)
                # store spotify_uri for each song
                if spotify_uri is not None:
                    self.all_song_info[video_title] = {
                        "youtube_url": youtube_url,
                        "song_name": song_name,
                        "artist": artist,
                        "spotify_uri": spotify_uri}

    def getSpotifyInfo(self, instructions):
        response = input(instructions)
        return response.strip()  # remove whitespace

        # create spotify playlist
    def create_playlist(self):
        # playlist metadata
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
        if len(songs) == 0:
            return None

        uri = songs[0]["uri"]
        return uri

    def add_songs_to_playlist(self):
        # populate all_song_info
        self.get_liked_videos()

        spotify_uris = []
        for song, info in self.all_song_info.items():
            spotify_uris.append(info["spotify_uri"])

        # create playlist
        playlist_id = self.create_playlist()
        # add all songs into new playlist
        request_data = json.dumps(spotify_uris)
        url = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id)

        response = requests.post(url, data=request_data, headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        })

        data = response.json()
        return data


def get_youtube_client():
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


def main():
    success = False
    print('\nDISCLAIMER: this only works for youtube videos that are a track or a part of a music album!\n')

    while not success:
        try:
            youtube_client = get_youtube_client()
        except Exception:
            print(
                '\nSeems like the Youtube OAuth token you provided was incorrect!\nTry again!\n')
            continue

        while not success:
            try:
                convert = CreatePlaylist(youtube_client)
                convert.add_songs_to_playlist()
                success = True
            except Exception:
                print(
                    '\nSeems like the Spotify details you provided were incorrect, do not match or have expired!\n')

    print('\nSuccess! Check your spotify account for a playlist called Liked YT Videos 😎.\n')


if __name__ == "__main__":
    main()
