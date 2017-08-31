import scrapy
import re
import musicbrainz, acousticbrainz_api

class VagalumePlaylistsSpider(scrapy.Spider):
    name = 'vagalumespider'
    start_urls = ['https://meu.vagalume.com.br/sitevagalume/']    

    def __init__(self):
        #self.count = 0
        CSV_HEADERS = ['source', 'user_id', 'track_name', 'artist_name', 'mbids', 'playlist_id', 'tags', 'playlist_name', 'date', \
                       'danceability_value', 'danceability_prob', 'gender_value','gender_prob', 'genre_dortmund_value', 'genre_dortmund_prob',\
                       'genre_electronic_value', 'genre_electronic_prob', 'genre_rosamerica_value', 'genre_rosamerica_prob', 'genre_tzanetakis_value',\
                       'genre_tzanetakis_prob', 'ismir04_rhythm_value', 'ismir04_rhythm_prob', 'mood_acoustic_value', 'mood_acoustic_prob', \
                       'mood_aggressive_value', 'mood_aggressive_prob', 'mood_electronic_value', 'mood_electronic_prob', 'mood_happy_value', \
                       'mood_happy_prob', 'mood_party_value', 'mood_party_prob', 'mood_relaxed_value', 'mood_relaxed_prob', 'mood_sad_value',\
                       'mood_sad_prob', 'moods_mirex_value', 'moods_mirex_prob', 'timbre_value', 'timbre_prob', 'tonal_atonal_value', \
                       'tonal_atonal_prob', 'voice_instrumental_value', 'voice_instrumental_prob']

        self.playlists_file = open('vagalume_playlists.csv', 'a')
        self.playlists_file.write("%s\n" % ",".join(CSV_HEADERS))
        self.acousticbrainz_api = acousticbrainz_api.AcousticBrainz()

    def parse_playlist(self, response):  
        for song in response.css('ol.songsList > li'):
            playlist_entry = song.css('a ::text').extract_first()
            if playlist_entry:
                vagalume_user = response.request.headers.get('Referer', None).rsplit("/", 2)[1]
                playlist_name = response.css('div.infoSongs > span.namePlay > b ::text').extract_first()
                playlist_id = response.url.rsplit("/", 2)[1]
                tags = []
                for tag in response.css('div.style > a'):                    
                    tags.append(tag.css('::text').extract_first())
                artist_name, track_name = playlist_entry.split(' - ',1)
                mbids = musicbrainz.retrieveMBID(track_name, artist_name)
                acoustic_data = {}
                if len(mbids) > 0:
                    try:
                        acoustic_data = self.acousticbrainz_api.get_track_data(mbids[0], 'high-level')
                    except:
                        pass

                csv_entry = ['vagalume', \
                            vagalume_user, \
                            '"%s"' % track_name.encode('utf-8'), \
                            '"%s"' % artist_name.encode('utf-8'),\
                            '"%s"' % str(mbids).encode('utf-8'),\
                            '"%s"' % playlist_id.encode('utf-8'),\
                            '"%s"' % ','.join(tags).encode('utf-8'),\
                            '"%s"' % playlist_name.encode('utf-8'), \
                            '"N/A"'.encode('utf-8'),\
                            '"%s"' % acoustic_data['highlevel']['danceability']['value'].encode('utf-8') if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['danceability']['probability'] if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['gender']['value'].encode('utf-8') if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['gender']['probability'] if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['genre_dortmund']['value'].encode('utf-8') if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['genre_dortmund']['probability'] if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['genre_electronic']['value'].encode('utf-8') if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['genre_electronic']['probability'] if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['genre_rosamerica']['value'].encode('utf-8') if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['genre_rosamerica']['probability'] if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['genre_tzanetakis']['value'].encode('utf-8') if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['genre_tzanetakis']['probability'] if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['ismir04_rhythm']['value'].encode('utf-8') if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['ismir04_rhythm']['probability'] if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['mood_acoustic']['value'].encode('utf-8') if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['mood_acoustic']['probability'] if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['mood_aggressive']['value'].encode('utf-8') if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['mood_aggressive']['probability'] if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['mood_electronic']['value'].encode('utf-8') if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['mood_electronic']['probability'] if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['mood_happy']['value'].encode('utf-8') if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['mood_happy']['probability'] if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['mood_party']['value'].encode('utf-8') if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['mood_party']['probability'] if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['mood_relaxed']['value'].encode('utf-8') if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['mood_relaxed']['probability'] if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['mood_sad']['value'].encode('utf-8') if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['mood_sad']['probability'] if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['moods_mirex']['value'].encode('utf-8') if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['moods_mirex']['probability'] if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['timbre']['value'].encode('utf-8') if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['timbre']['probability'] if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['tonal_atonal']['value'].encode('utf-8') if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['tonal_atonal']['probability'] if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['voice_instrumental']['value'].encode('utf-8') if len(acoustic_data) > 0 else "",\
                            '"%s"' % acoustic_data['highlevel']['voice_instrumental']['probability'] if len(acoustic_data) > 0 else "",\
                            ]
                self.playlists_file.write('%s\n' % ','.join(csv_entry))

    def parse(self, response):
        # Initially crawling from sitevagalume profile
        for post in response.css('ul.listContent > li.partInfo'):
            playlist_url = post.css('div.infoPlay > a ::attr(href)').extract_first()
            yield scrapy.Request(response.urljoin(playlist_url), callback=self.parse_playlist, body='teste')
        
        with open("vagalume_users.txt") as f:
            for follower in f.readlines():
                yield scrapy.Request(response.urljoin('https://meu.vagalume.com.br/%s/' % follower), callback=self.parse)
        
