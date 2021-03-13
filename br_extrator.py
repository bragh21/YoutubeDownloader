import requests as req
from json import loads as JSloads
from json import dumps as JSdumps

def playlist_videoId(url) -> list:
    """Processa o link da playlist, e encontra os videos que fazem parte dela.
    
    :param str url:
        Uma URL de playlist válida.
    :return list:
        Index 0 -> Nome da Playlist
        Index1 -> Dict contendo os videoIds como chaves e os seus respectivos nomes como valores
    """
    if not 'playlist' in url.lower():
        print("Link não é um link de playlist. Verifique.")
        return None

    response = req.get(url)

    text_response = response.text
    info_videos = dict()

    ## Encontra o script js que contem objeto ytInitialData. Nele estão os links.
    if 'ytInitialData' in text_response:
        index_init = text_response.find("ytInitialData")+16
        index_final = text_response.find('</script>', index_init)-1
        script = text_response[index_init:index_final]
    else: 
        print('Não encontrado objeto ytInitialData no retorno. Verifique')
        exit(0)

    # ytInicialData é um objeto JavaScript, que pode ser lido com um JSON.
    # Logo, é isso que faremos, buscando as subchaves, até chegar no na chave
    # contents, que é uma lista Python contendo as propriedades de cada video,
    # como o seu id, que será utilizado para identifica-lo
    temp = JSloads(script)
    playlist_title = temp.get("metadata").get("playlistMetadataRenderer").get("title")
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