import json
import youtube_dl
#import matplotlib.pyplot as plt

from pathlib import Path
#from slugify import slugify

with open('hoerbert.json', 'r', encoding='utf-8') as f:
    hoerbert = json.load(f)

destination = Path('sd_card')
destination.mkdir(exist_ok=True, parents=True)

for idb, button in enumerate(hoerbert):
    for ids, song in enumerate(hoerbert[button]):
        #if idb != 6 or ids != 3:
        #    continue 
        song_name = '%d.%%(ext)s' % (ids)
        song_path = destination / str(idb) / song_name
        song_path_mp3 = destination / str(idb) / ('%d.mp3' % (ids))
        
        print('\n%s\n%s\n' % (song['Name'], '=' * len(song['Name'])))

        if song_path_mp3.exists():
            print('Song exists, continue\n')
            continue
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(song_path),
            'postprocessors': [
                {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
                }
            ],
            'postprocessor_args' : []
            }

        if len(song['crop_start']) > 0:
            ydl_opts['postprocessor_args'].extend(['-ss', song['crop_start']])

        if len(song['crop_tail']) > 0:
            ydl_opts['postprocessor_args'].extend(['-to', song['crop_tail']])

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.cache.remove()
            ydl.download([song['Link']])