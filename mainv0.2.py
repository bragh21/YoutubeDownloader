from pytube import YouTube
from br_extrator import *
from os import path, mkdir, chdir, getcwd, system
from datetime import datetime as dt
from sys import path as sysPath
from pathlib import Path
from conversor import extrair_audio


MARGEM = " "
def main():
  system("@echo off")
  system("cls")
  link = input(f"{MARGEM}Entre com a URL do vídeo: ")
  converter = input(f"{MARGEM}Deseja converter em MP3? [S/N]: ") or "s"

  if 's' in converter.lower():
    manter = input(f"{MARGEM}Manter arquivos de vídeo após a conversão? [N/S]: ") or "n"
    
    if 's' in manter.lower():
      manter = True
    else:
      manter = False

  if 'music' in link:
    link = link.replace("music.", "")

  if not 'youtube' in link:
    print(f"{MARGEM}Link não é uma URL do Youtube. Verifique.")
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
      print(f"{MARGEM}\nDetectamos que o diretorio {playlistName} já existe no diretorio atual")
      hr_atual = dt.today().now().strftime("%d-%m-%Y_%H-%M-%S")
      print(f"{MARGEM}Será criado um diretorio {playlistName}_{hr_atual}")
      dir_path = playlistName + "_" + hr_atual
      mkdir(dir_path)
      chdir(dir_path)

    system("cls")
    print(f"{MARGEM}\nRealizando download dos vídeos")
    cont = 1
    for videoId, videoName in info_videos.items():
      url_video = 'https://www.youtube.com/watch?v=' + videoId
      video = YouTube(url_video) 
      stream = video.streams.get_highest_resolution()

      print(f"{MARGEM}{cont} - {videoName}", end="", flush=True)
      stream.download()
      print(" =====> CONCLUÍDO")

      if 's' in converter.lower():
        print(f"{MARGEM}{MARGEM}Convertendo {videoName}", end="", flush=True)
        extrair_audio(str(Path(getcwd(), stream.default_filename.replace("'", ""))), manter)
        print(" =====> CONCLUÍDO")
      print()
      cont+=1

  else:
    if not path.exists('Downloads_YouTube'):
      mkdir('Downloads_YouTube')
      chdir('Downloads_YouTube')
    else:
      chdir('Downloads_YouTube')

    video = YouTube(link)
    stream = video.streams.get_highest_resolution()
    system("cls")
    print(f"{MARGEM}Realizando download de video")
    print(f"{MARGEM}{video.title}", end="", flush=True)
    stream.download()
    print(" =====> CONCLUÍDO")
    
    if 's' in converter.lower():
      print(f"{MARGEM}Convertendo {video.title}", end="", flush=True)
      extrair_audio(str(Path(getcwd(), stream.default_filename.replace("'", ""))), manter)
      print(" =====> CONCLUÍDO")
    
    print()

  print(f"{MARGEM}Download finalizado.")
  

if __name__ == "__main__":
  while True:
    main()
    opc = input(f"{MARGEM}{'#':#^100}\n{MARGEM}SAIR? [S/N]: ").strip().lower() or "n"
    if 's' in opc:
      print(f"{MARGEM}Obrigado por usar o Youtube Downloader!")
      break

  system(f"explorer /select, {Path(getcwd())}")
  exit(0)