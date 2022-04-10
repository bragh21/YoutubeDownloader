import json
from pytube import YouTube
from br_extrator import *
from os import path as ospath, mkdir, chdir, getcwd, system
from datetime import datetime as dt
from sys import path as sysPath
from pathlib import Path
from conversor import extrair_audio

class Downloader:
  def __init__(self) -> None:
    
    system("@echo off")
    system("cls")
    self.BASE_DIR = Path(sysPath[0])
    self.PREF_FILE_DIR = str(Path(self.BASE_DIR, "userprofile.json"))
    self.MAKE_NEW_PREFS = False
    self.ANONYMOUS = False
    self.USING_PREFS = False
    self.CONVERT_MP3 = True
    self.SAVE_ORIGINALS = False
    self.OPTIONS = ["convert_mp3", "save_originals"]
    self.ROOT_FOLDER = str(Path(self.BASE_DIR,"Downloads_YouTube")) 
    self.load_prefs()
  
  def load_prefs(self):
    # Verifica se existe um arquivo de preferencias de usuário, e solicita para ser carregar o arquivo.
    if ospath.exists(self.PREF_FILE_DIR):
      with open(self.PREF_FILE_DIR, 'r') as fl:
        try:
          prefs = json.loads(fl.read())
          prefs: dict
        except Exception as err:
          prefs = None
          self.MAKE_NEW_PREFS = True
          print("[ERRO] Foi encontrado um arquivo de preferencias, porem nao foi possível carrega-lo.")
          print(f"[ERRO] Arquivo: {self.PREF_FILE_DIR}")
          print(f"[ERRO] Detalhes do erro: {err}")
          print(f"[ERRO] Detalhes do erro: {err.args}\n")
        else:
          print("Encontrado arquivo de preferencias:")
          print("-----------------------------------------------------")
          for pref, value in prefs.items():
            if pref in self.OPTIONS:
              msg = pref + ": " + str(bool(value))
              print(f"| {msg:<50}|")
            else:
              msg = 'Unrecognized option ' + pref + ": " + str(value)
              print(f"| {msg:<50}|")
          print("-----------------------------------------------------\n")
      
    if prefs:
      load_pref = input("Deseja usar essas preferências nessa sessao? [S/N]: ") or 's'
      if 's' in load_pref.lower():
        self.CONVERT_MP3 = prefs.get("convert_mp3", self.CONVERT_MP3)
        self.SAVE_ORIGINALS = prefs.get("save_originals", self.SAVE_ORIGINALS)
      else:
        make_pref = input("Deseja sobreescrever as preferencias baseado nessa sessao? [S/N]: ") or 's'
        if 's' in make_pref.lower():
          self.MAKE_NEW_PREFS = True
        else:
          self.ANONYMOUS = True
      
    # Se o arquivo não existir, ou se o usuario desejar sobreescrever o arquivo, solicita as preferencias. 
    if not ospath.exists(self.PREF_FILE_DIR) or self.MAKE_NEW_PREFS or self.ANONYMOUS:
      
      converter = input("Deseja converter em MP3? [S/N]: ") or "s"
      if 's' in converter.lower():
        self.CONVERT_MP3 = True
        manter = input("Manter arquivos de vídeo após a conversão? [S/N]: ") or "n"
        
        if 's' in manter.lower():
          self.SAVE_ORIGINALS = True
        else:
          self.SAVE_ORIGINALS = False
          
      else:
        self.CONVERT_MP3 = False
        self.SAVE_ORIGINALS = False
      
      if not ospath.exists(self.PREF_FILE_DIR) or self.MAKE_NEW_PREFS:
        with open(self.PREF_FILE_DIR, 'w') as new_fl:
          new_prefs = {"convert_mp3": self.CONVERT_MP3, "save_originals": self.SAVE_ORIGINALS}
          new_fl.write(json.dumps(new_prefs))
          new_fl.close()
  
  def start_download(self): 
    # Inicia a solicitação pela URL do vídeo
    link = input("Entre com a URL do vídeo: ")
    
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

      playlistName = info[0]
      info_videos = info[1]

      # Oganização dos diretorios para download:
      if not ospath.exists(self.ROOT_FOLDER):
        mkdir(self.ROOT_FOLDER)
        chdir(self.ROOT_FOLDER)
      else:
        chdir(self.ROOT_FOLDER)

      if not ospath.exists(playlistName):
        mkdir(playlistName)
        chdir(playlistName)
      else:
        print(f"\nDetectamos que o diretorio {playlistName} já existe no diretorio atual")
        hr_atual = dt.today().now().strftime("%d-%m-%Y_%H-%M-%S")
        dir_path = playlistName + "_" + hr_atual
        print(f"Será criado um diretorio {dir_path}")
        mkdir(dir_path)
        chdir(dir_path)

      system("cls")
      print("Realizando download dos vídeos")
      for videoId, videoName in info_videos.items():
        url_video = 'https://www.youtube.com/watch?v=' + videoId
        video = YouTube(url_video) 
        stream = video.streams.get_highest_resolution()

        print(f"{videoName}", end="", flush=True)
        stream.download()
        print(" =====> CONCLUÍDO")

        if self.CONVERT_MP3:
          print(f"Convertendo {videoName}", end="", flush=True)
          extrair_audio(str(Path(getcwd(), stream.default_filename.replace("'", ""))), self.SAVE_ORIGINALS)
          print(" =====> CONCLUÍDO")
        print()

    else:
      if not ospath.exists(self.ROOT_FOLDER):
        mkdir(self.ROOT_FOLDER)
        chdir(self.ROOT_FOLDER)
      else:
        chdir(self.ROOT_FOLDER)

      video = YouTube(link)
      stream = video.streams.get_highest_resolution()
      system("cls")
      print("Realizando download de video")
      print(f"{video.title}", end="", flush=True)
      stream.download()
      print(" =====> CONCLUÍDO")
      
      if self.CONVERT_MP3:
        print(f"Convertendo {video.title}", end="", flush=True)
        extrair_audio(str(Path(getcwd(), stream.default_filename.replace("'", ""))), self.SAVE_ORIGINALS)
        print(" =====> CONCLUÍDO")
      
      print()

    print("Download finalizado.")
    chdir(self.BASE_DIR)

if __name__ == "__main__":
  while True:
    app = Downloader()
    app.start_download()
    opc = input("\nSAIR? [S/N]: ").strip().lower() or "n"
    if 's' in opc:
      system("cls")
      print("Obrigado por usar o Youtube Downloader!")
      break

  system(f"explorer /select, {app.ROOT_FOLDER}")
  exit(0)