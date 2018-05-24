#! /usr/bin/env python 
import csv 
import sys
import spotipy
import spotipy.util as util
import smtplib
import requests
import json
from pprint import pprint

res = requests.get('https://socast-public.s3.amazonaws.com/player/np_36_.js')
musicDict = json.loads(res.text[14:-2]) # 'jsonpcallback(' ... ');'
songTitles = musicDict['song_name']
songArtist = musicDict['artist_name']
sp = spotipy.Spotify()
username = '' 
client_id = ''
client_secret = ''
redirect_uri ='http://localhost:/callback'
playlist_id = '2VMrZXn5wam91eG2G7qHVJ'
smtpObj = smtplib.SMTP('smtp.gmail.com',587)
smtpObj.starttls()
smtpObj.ehlo()
smtpObj.login('','') 

outputfile = open('edgesongs.csv' ,'a')
outputread = open('edgesongs.csv','r')
reader = csv.reader(outputread)
writer =csv.writer(outputfile)
data = list(reader)
i = 0
while i < len(data): 
    if (data[i][0] == songTitles) and (data[i][1] == songArtist):
        smtpObj.sendmail('xxmrmau5@gmail.com','xxmrmau5@gmail.com','song was already on playlist')
        sys.exit()
    i =i + 1
writer.writerow([songTitles,songArtist])

track_id = sp.search(songArtist + " " + songTitles,limit=1,type='track',)
try:
    track_id=track_id['tracks']['items'][0]['id']
except IndexError:
    smtpObj.sendmail('xxmrmau5@gmail.com','xxmrmau5@gmail.com','unable to find song')
real_id=[track_id]
##need to add track id as a iterable or else the sp.user_playlist_add_tracks() will iterate through tthe track id and produce an error
scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username, scope, client_id, client_secret,redirect_uri)

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.user_playlist_add_tracks(username, playlist_id, real_id)
    smtpObj.sendmail('xxmrmau5@gmail.com','xxmrmau5@gmail.com',' added song to playlist')
else:
    smtpObj.sendmail('xxmrmau5@gmail.com','xxmrmau5@gmail.com','cannot get token')
