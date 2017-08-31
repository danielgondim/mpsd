# -*- coding: utf-8 -*-
import urllib2, xmltodict

from unidecode import unidecode

API_REST_MUSICBRAINZ = "http://musicbrainz.org/ws/2/recording/?query="

def retrieveMBID(songName, artistName):
  songQuoted = urllib2.quote(songName.replace('/', ' ').encode('utf8'))
  try:
    file = urllib2.urlopen(API_REST_MUSICBRAINZ + songQuoted)
    xml = file.read()
    file.close()
    doc = xmltodict.parse(xml)
    listOfRecordings = doc['metadata']['recording-list']['recording']
    listOfMBIDs = []
    MBID_found = False

    songName = ''.join(e for e in songName if e.isalnum())
    artistName = ''.join(e for e in artistName if e.isalnum())

    for record in listOfRecordings:
      if type(record) == unicode:

        retrieved_artist_name = unidecode(listOfRecordings['artist-credit']['name-credit']['artist']['name']).lower()
        retrieved_song_name = unidecode(listOfRecordings['title']).lower()
        retrieved_artist_name = ''.join(e for e in retrieved_artist_name if e.isalnum())
        retrieved_song_name = ''.join(e for e in retrieved_song_name if e.isalnum())

        if (((retrieved_artist_name in artistName.lower) or
            (artistName in retrieved_artist_name))
          and ((retrieved_song_name in songName) or (songName in retrieved_song_name))):
            listOfMBIDs.append(listOfRecordings['@id'])
            MBID_found = True
        break
      else:
        currentArtistList = record['artist-credit']['name-credit']
        if type(currentArtistList) == type([]):
          for currentArtist in currentArtistList:
            retrieved_artist_name = unidecode(currentArtist['artist']['name']).lower()
            retrieved_song_name = unidecode(record['title']).lower()
            retrieved_artist_name = ''.join(e for e in retrieved_artist_name if e.isalnum())
            retrieved_song_name = ''.join(e for e in retrieved_song_name if e.isalnum())
            if (((retrieved_artist_name in artistName.lower()) or
                (artistName.lower() in retrieved_artist_name))
              and ((retrieved_song_name in songName.lower()) or (songName.lower() in retrieved_song_name))):
              listOfMBIDs.append(record['@id'])
              MBID_found = True
              break
        else:

          retrieved_artist_name = unidecode(currentArtistList['artist']['name']).lower()
          retrieved_song_name = unidecode(record['title']).lower()
          retrieved_artist_name = ''.join(e for e in retrieved_artist_name if e.isalnum())
          retrieved_song_name = ''.join(e for e in retrieved_song_name if e.isalnum())

          if (((retrieved_artist_name in artistName.lower()) or
              (artistName.lower() in retrieved_artist_name))
            and ((retrieved_song_name in songName.lower()) or (songName.lower() in retrieved_song_name))):
              listOfMBIDs.append(record['@id'])
              MBID_found = True
              break 
      if MBID_found:
        break    
    return listOfMBIDs
  except:
    return []