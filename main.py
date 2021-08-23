from pytube import YouTube
from br_extrator import *
from os import path, mkdir, chdir, getcwd
from datetime import datetime as dt
from sys import path as sysPath
from pathlib import Path
from conversor import extrair_audio

link = input("Entre com a URL do vídeo: ")
converter = input("Deseja converter em MP3? [S/N]: ") or "n"

if 's' in converter.lower():
  manter = input("Manter arquivos de vídeo após a conversão? [S/N]: ") or "n"
  
  if 's' in manter.lower():
    manter = True
  else:
    manter = False

if 'music' in link:
  link = link.replace("music.", "")

if not 'youtube' in link:
  print("Link não é uma URL do Youtube. Verifique.")
  exit(1)

## Trata link de playlist
if 'playlist' in link:
  info = playlist_videoId(link)

  if "None" in str(type(info)):
    exit(1)

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
    print(f"\nDetectamos que o diretorio {playlistName} já existe no diretorio atual")
    hr_atual = dt.today().now().strftime("%d-%m-%Y_%H-%M-%S")
    print(f"Será criado um diretorio {playlistName}_{hr_atual}")
    dir_path = playlistName + "_" + hr_atual
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

    if 's' in converter.lower():
      print(f"Convertendo {videoName}", end="")
      extrair_audio(str(Path(getcwd(), stream.default_filename.replace("'", ""))), manter)
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
  print(" =====> CONCLUÍDO")
  
  if 's' in converter.lower():
    print(f"Convertendo {video.title}", end="")
    extrair_audio(str(Path(getcwd(), stream.default_filename.replace("'", ""))), manter)
    print(" =====> CONCLUÍDO")