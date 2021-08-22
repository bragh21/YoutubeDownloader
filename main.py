from pytube import YouTube
from br_extrator import *
link = input("Entre com a URL do vídeo: ")
from os import path, mkdir, chdir

## Trata link de playlist
if 'playlist' in link:
    info = playlist_videoId(link)

    if "None" in str(type(info)):
        exit(0)

    playlistName = info[0].strip().replace(' ', '_')
    info_videos = info[1]

    # Oganização dos diretorios para download:
    if not path.exists('Downloads_YouTube'):
        mkdir('Downloads_YouTube')
        chdir('Downloads_YouTube')
    else:
        chdir('Downloads_YouTube')
        
    if not path.exists(playlistName):
        mkdir(playlistName)
        chdir(playlistName)
    else:
        print(f"\nDetectamos que o diretorio {playlistName} já exsite no diretorio atual")
        print(f"Será criado um diretorio {playlistName}_1")
        dir_path = playlistName + "_1"
        mkdir(dir_path)
        chdir(dir_path)


    print("Realizando download dos vídeos")
    for videoId, videoName in info_videos.items():
        url_video = 'https://www.youtube.com/watch?v=' + videoId
        video = YouTube(url_video) 
        stream = video.streams.get_highest_resolution()

        
        print(f"{videoName}", end="")
        stream.download()
        print(" =====> CONCLUÍDO")
else:
    if not path.exists('Downloads_YouTube'):
        mkdir('Downloads_YouTube')
        chdir('Downloads_YouTube')
    else:
        chdir('Downloads_YouTube')

    video = YouTube(link)
    stream = video.streams.get_highest_resolution()
    print("Realizando download de video")
    print(f"{video.title}", end="")
    stream.download()
    print(" =====> CONCLUÍDO\n")
   