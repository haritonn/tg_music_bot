import yt_dlp 

async def install_from_link(url: str):
    """Searching and installing .mp3 file from video with specified URL"""

    output_path = 'install_path/%(title)s.%(ext)s'

    ydl_params = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
    }

    with yt_dlp.YoutubeDL(params=ydl_params) as ydl:
        info = ydl.extract_info(url, download = True)
        filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
    
    return filename


async def install_from_name(query: str):
    """Searching 10 best matches via specified query"""

    search_query = f'ytsearch10:{query}'
    output_path = 'install_path/%(title)s.%(ext)s'

    ydl_searchparams = {
        'quiet': True, 
        'extract_flat': True
    }

    with yt_dlp.YoutubeDL(params = ydl_searchparams) as ydl:
        info = ydl.extract_info(search_query, download = False)
        results = info.get('entries', [])

    return [[video['url'], video['title']] for video in results]
        