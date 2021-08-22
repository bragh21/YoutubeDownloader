import requests
from json import JSONDecodeError, loads

link = "https://www.youtube.com/watch?v=R98MHlsbUeU"

result = requests.get(link)

headers = str(result.headers).replace("'","$").replace('$','"')
print(f"\nStatus Code: {result.status_code}\n")
print(f"Headers: {result.headers}\n")
print(f"Encoding: {result.encoding}\n")
print("TEXTO >>>")

print(f"{result.text}")
print("\nJSON >>>")
try:
  print(f"{result.json()}")
except JSONDecodeError:
  print("Nenhum conteúdo JSON disponível.")
