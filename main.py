#!/usr/bin/env python3
# coding: utf-8


# MODULES
import os # path, getenv, mkdirs
import sys # executable
import json # dump, load
import subprocess # run, check_output


# GLOBALS
USR = os.getenv('SPOTIPY_CLIENT_ID') # user environement variable, must be set as SPOTIPY_CLIENT_ID
PASSWD = os.getenv('SPOTIPY_CLIENT_SECRET') # user environment variable, must be set as SPOTIPY_CLIENT_SECRET
PATH = os.path.abspath('.') # path to current directory


# Create or fetch playlists to scrape
playlists = []
if not os.path.isfile(PATH + '\\playlists.json'):
    with open(PATH + '\\playlists.json', 'w+') as ppath:
        json.dump({"playlists":"https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF"}, ppath) # default: Global Top 50
        playlists = ['https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF']
else:
    with open(PATH + '\\playlists.json', 'r') as ppath:
        playlists = [p for p in json.load(ppath)['playlists']]


# Create directories for program output
if not os.path.isdir(PATH + '\\spectrogram'):
    os.makedirs(PATH + '\\spectrogram')

if not os.path.isdir(PATH + '\\playlists'):
    os.makedirs(PATH + '\\playlists')


# Serves as the primary script controller using subprocesses
def main():

    # Runs metadata extraction, local playlist downloads, and spectrogram analysis in sequence per playlist
    # sys.executable is necessary to ensure venv is still being run for all subprocesses
    for playlist_id in playlists:
        playlist_name = subprocess.check_output([sys.executable, 'get_md.py', USR, PASSWD, playlist_id.split('/')[-1]])
        playlist_name = playlist_name.decode('utf-8')[:-2] # inclusive for non-US English characters
        subprocess.run(['powershell.exe', '.\\get_songs.ps1', playlist_id]) # ensure powershell scripts are set for RemoteSigned
        subprocess.run([sys.executable, 'get_spectrogram.py', playlist_name], shell = True)

if __name__ == '__main__':
    main()