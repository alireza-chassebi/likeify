# Likeify

---

CLI tool that automates the conversion of your liked videos on youtube into a spotify playlist.

   <br />

## Prerequisites

---

Brefore you begin, ensure you have met the following requirements:

- You have [Python](https://www.python.org/downloads/) installed
- You have [pip](https://pip.pypa.io/en/stable/) installed

   <br />

## Installing Likeify

---

To install Likeify, do the following:

1. clone the repo

```
  git clone https://github.com/alireza-chassebi/websocket-editor
```

2. navigate to Likeify root directory

3. setup the virtual environment

```
  python3 -m venv env
```

4. activate virtual environment

```
  source env/bin/activate
```

5. install dependencies in the virtual environment

```
  pip3 install -r requirements.txt
```

   <br />

## Setting up client_secret.json

1. go to googles developer [console](https://console.developers.google.com/apis/credentials) credentials section after signing in

2. click Create Credentials then OAuth Client ID

3. fill the form accordingly then click create:

- Application Type: Desktop Application
- Name: ANYNAME

4. populate **client_secret.json** with the **Client ID** and **Client Secret** provided by the console

   <br />

## Running Likeify

---

To run the app, do the following:

1. navigate to the projects root directory

2. activate the virtual environment

```
  source env/bin/activate
```

3. run the python script create_playlist.py

```
  python3 create_playlist.py
```

4. follow the instructions carefully 😎.

5. And check your spotify playlists after.

   <br />

## Disclaimer

---

This only works for youtube videos that are a track or a part of a music album!
