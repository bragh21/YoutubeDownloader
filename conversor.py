from os import chdir, getcwd, listdir, remove
from pathlib import Path
from sys import path as sysPath
import subprocess


FFMPEG = Path(sysPath[0], "ffmpeg.exe")

def extrair_audio(path_video: str, manter_original=False):
  index_ext = path_video.find(".", -5)
  EXT_ORIG = path_video[index_ext:]
  audio = path_video.replace(EXT_ORIG, ".mp3")

  subprocess.call(f'{FFMPEG} -loglevel +quiet -i "{path_video}" "{audio}"')
  if not manter_original:
    remove(path_video)

def __old__():

  origem = input("Informe o local onde estão os arquivos de video: ") or ""

  if len(origem) == 0:
    print("Você não informou um diretorio. Saindo...")
    quit()

  try:
    get_back = getcwd()
    chdir(origem)
  except FileNotFoundError:
    print(f"O diretorio {origem} não existe, está incorreto, ou inacessível.")
  else:
    chdir(get_back)

  # Coltando os arquivos de video
  EXT_SRC = '.mp4' # para buscar outro formato de video, altere a constante.
  EXT_DST = '.wav' # mude para converter para outro formato

  videos = [file for file in listdir(origem) if file.endswith(EXT_SRC)]

  for video in videos:
    abs_video = origem + "\\" + video
    audio = origem + "\\" + video.replace(EXT_SRC, EXT_DST)
    subprocess.run(f"{FFMPEG} -i {abs_video} {audio}")

  print('Conversão concluida.')
  print(f'Verifique em {origem}')
  '''
  C:\COMPARTILHADO\Radios_GTA\
  src = '"C:\\Users\\user\\OneDrive_Pessoal\\OneDrive\\Projetos\\Six Days (Remix)-5JhKWFxLhKo.mp4"'
  dst = src + ".mp3"

  subprocess.run(f"./ffmpeg/bin/ffmpeg.exe -i {src} {dst}")
  '''
