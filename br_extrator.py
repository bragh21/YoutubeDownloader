import requests as req
from json import loads as JSloads
from json import dumps as JSdumps


def playlist_videoId(url) -> list:
  """Processa o link da playlist, e encontra os videos que fazem parte dela.

  :param str url: Uma URL de playlist válida.
  :return list: [Nome da Playlist, Dict contendo os videoIds e os seus respectivos nomes]
  """
  response = req.get(url)

  if response.status_code != 200:
    print("Não foi possivel coletar informações.")
    print(f"HTTP Code: {response.status_code}")
    return None

  text_response = response.text
  info_videos = dict()

  ## Encontra o script js que contem objeto ytInitialData. Nele estão os links.
  if 'ytInitialData' in text_response:
    index_init = text_response.find("ytInitialData")+16
    index_final = text_response.find('</script>', index_init)-1
    script = text_response[index_init:index_final]
  else: 
    print('Não encontrado objeto ytInitialData no retorno. Verifique')
    return None

  # ytInicialData é um objeto JavaScript, que pode ser lido com um JSON.
  # Logo, é isso que faremos, buscando as subchaves, até chegar no na chave
  # contents, que é uma lista Python contendo as propriedades de cada video,
  # como o seu id, que será utilizado para identifica-lo
  temp = JSloads(script)
  # with open('script.js', 'w') as fl:
  #     fl.write(JSdumps(temp))

  # Se a playlist não for pública, o pytube não a encontrará.
  if "alerts" in temp.keys():
    erro = temp.get("alerts")[0]

    if "alertRenderer" in erro.keys():
      erro1 = erro.get("alertRenderer").get("text").get("runs")[0].get("text")
      print("Não foi possivel encontrar a playlist informada.")
      print("Certifique-se de que a playlist é pública, e tente novamente.")
      return None

    else:
      print("Erros desconhecidos identificados. Verifique em 'script.js'")
      with open('script.js', 'w') as fl:
        fl.write(JSdumps(temp))
      return None

  playlist_title = temp.get("metadata").get("playlistMetadataRenderer").get("title").replace('"','')
  temp1 = temp.get('contents').get("twoColumnBrowseResultsRenderer")
  temp2 = temp1.get('tabs')[0].get("tabRenderer")
  temp3 = temp2.get("content").get("sectionListRenderer").get("contents")[0]
  temp4 = temp3.get("itemSectionRenderer").get("contents")[0].get("playlistVideoListRenderer")
  obj_videos = temp4.get("contents")

  # Armazena o videoId e o Nome do video para realizar o download.
  for video_prop in obj_videos:
    # info_videos = video_prop
    videoId = video_prop.get("playlistVideoRenderer").get("videoId")
    videoName = video_prop.get("playlistVideoRenderer").get("title").get("runs")[0].get("text")
    info_videos[videoId] = videoName

  return [playlist_title, info_videos]