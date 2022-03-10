# Copyright (C) 2022 The Authors
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# This script won't run Paperplane, it just generates a session for Google Drive.
#

import os
import sys
from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import SpotifyOAuth


def main():
    load_dotenv("../config.env")

    print(
        "Go to the Spotify Developer Dashboard, create a new app, making sure to set the redirect "
        "URL to https://google.com (IMPORTANT!), and then copy the client ID and client secret into "
        "your config.env or environment variables. You will then see a link here, "
        "which you will need to open for authenticating with Spotify. After authenticating, copy the whole "
        "link you are redirected to (including the long string after ?) and paste it in this window. "
        "A spotify_session file will be generated and it will also be printed for the SPOTIFY_SESSION "
        "environment variable.")

    if not os.environ.get("SPOTIPY_CLIENT_ID") or not os.environ.get("SPOTIPY_CLIENT_SECRET"):
        print("You need to set your SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET in config.env or envvars! Halting!")
        sys.exit(1)

    client = spotipy.Spotify(
        auth_manager=spotipy.oauth2.SpotifyOAuth(
            redirect_uri="https://google.com",
            scope="user-read-playback-state",
            open_browser=False,
            cache_handler=spotipy.oauth2.CacheFileHandler(
                cache_path="../spotify_session"
            ),
        )
    )

    client.current_user()

    with open('../spotify_session', 'r') as file:
        print(file.read())


if __name__ == "__main__":
    main()
