import yt_dlp 
from bs4 import BeautifulSoup
import urllib.parse
import requests

async def install_from_link(url: str):
    """Searching and installing .mp3 file from video with specified URL"""


    ydl_params = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '145'
        }],
    }

    with yt_dlp.YoutubeDL(params=ydl_params) as ydl:
        info = ydl.extract_info(url, download = True)
        filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3').replace('.opus', '.mp3')
    
    return filename


async def install_from_name(query: str):
    query = urllib.parse.quote(query, safe='')
    search_link = f'https://soundcloud.com/search?q={query}'

    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(search_link, headers =  headers)

    if response.status_code == 200:
        bs = BeautifulSoup(response.text, 'html.parser')
        res = bs.find_all('a')[6:-7]

        for i in range(0, len(res)):
            res[i] = str(res[i])[9:].replace('">', ' ').replace('</a>', '').replace(' ', '@', 1).split(sep='@')
            if len(res[i][1]) >= 32:
                res[i][1] = res[i][1][:63]

    return res



        