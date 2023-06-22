import requests
import matplotlib.pyplot as plt
import matplotlib.image
import io
import os

"""headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': "ef7e9b83b25359c08ef9f5135245bf8d"}
params = {"fixture":"971185"}
url = "https://v3.football.api-sports.io/predictions"
respuesta = requests.get(url, params=params, headers=headers).json()["response"]

print(respuesta)"""

respuesta = requests.get(url = "https://media-2.api-sports.io/football/teams/451.png")
archivo_en_bytes = io.BytesIO(respuesta.content)
imagen = matplotlib.image.imread(archivo_en_bytes, format = "jpg")
plt.imshow(imagen)
plt.title("Boquita el más grande papá")
plt.show()
