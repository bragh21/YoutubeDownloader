import requests

BASE_URL = "https://music.youtube.com/youtubei/v1/browse?"

query = "ctoken=4qmFsgJhEiRWTFBMRXNKMjhVZXpzUUFqQm14LVNlandfNUFzY1VickJMUjMaFENBRjZCbEJVT2tOSFVRJTNEJTNEmgIiUExFc0oyOFVlenNRQWpCbXgtU2Vqd181QXNjVWJyQkxSMw%3D%3D"
query = query + "&alt=json"
query = query + "&key=VLPLEsJ28UezsQAjBmx-Sejw_5AscUbrBLR3"


_url = BASE_URL + query

response = requests.post(_url)
print(response.text)

# ctoken=4qmFsgJ5Eg1GRW11c2*****AwY0RGdg%253D%253D&itct=CCYQyb*****h0LqwUa
# &alt=json&key=AIzaSyC*****dJoCTL-WE*****30


