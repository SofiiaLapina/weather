import requests
from minio import Minio

client = Minio(
    "bucket.railway.internal:9000",
    access_key="J9OwcuItDPy29BCpLVKZv19Ztsq6gZdL",
    secret_key="oORnzoR4BJrPre88Nrg0OUyYrcfOs7B6zlcF7RsjIC3uAk3J",
    secure=False
)

API_KEY = '4f190d24ad0b38c083d7f0b3d7246279'
city = 'Kyiv'
weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
response = requests.get(weather_url)
data = response.json()

icon_code = data['weather'][0]['icon']
icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
img_data = requests.get(icon_url).content

with open('weather_icon.png', 'wb') as handler:
    handler.write(img_data)

bucket_name = "weathertest"
if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)
client.fput_object(bucket_name, "weather_icon.png", "weather_icon.png")

print("Картинка успішно завантажена в MinIO на Railway")
