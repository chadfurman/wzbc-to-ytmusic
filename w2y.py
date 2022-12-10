import scrapy
from ytmusicapi import YTMusic
from scrapy.crawler import CrawlerProcess

yt = YTMusic(auth="./headers")
headers_file = open('./headers_raw')

print('...starting...')
class WzbcPlaylistScraper(scrapy.Spider):
    name='wzbc-scraper'
    start_urls=[
        'https://spinitron.com/WZBC/pl/16747045/Malleus-Vibrations'
        # 'https://spinitron.com/WZBC/pl/16747964/Escape-Plan'
        
    ]

    def parse(self, response):
        items=[]
        for spin in response.css('.spin-item'):
            artist=spin.css('.artist::text').get()
            song=spin.css('.song::text').get()
            album=spin.css('.release::text').get()
            item={
                'artist': artist,
                'song': song,
                'album': album,
            }
            items.append(item)

        playlist_name = response.css('.show-title a::text').get()
        self.process_items(playlist_name, items)

    def process_items(self, playlist_name, items):
        print('processing items')
        playlist_items = []
        for item in items:
            results = yt.search(query=item['song'],filter='songs')
            for result in results:
                if not result['artists'][0]['name'] == item['artist']:
                    continue
                else:
                    playlist_items.append(result['videoId'])
                    break
        playlist_id = self.get_or_create_playlist_id(playlist_name)
        print('playlist id')
        print(playlist_id)
        print('playlist items')
        print(playlist_items)
        print(yt.add_playlist_items(playlist_id, playlist_items))

    def get_or_create_playlist_id(self, playlist_name):
        print('getting playlist')
        yt.setup(filepath='./headers', headers_raw=headers_file.read())
        playlists = yt.get_library_playlists(limit=None)
        print('playlists')
        print(playlists)
        for playlist in playlists:
            if playlist['title'] == playlist_name:
                return playlist['playlistId']
        print('creating playlist')
        return yt.create_playlist(playlist_name, "WZBC Playlist", privacy_status="PUBLIC")
        

process = CrawlerProcess()
process.crawl(WzbcPlaylistScraper)
process.start()