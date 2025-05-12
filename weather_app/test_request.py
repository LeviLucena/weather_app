import requests

url = "http://localhost:5000/fetch_weather"
payload = {
    "latitude": -23.55,
    "longitude": -46.63,
    "city": "São Paulo"
}

response = requests.post(url, json=payload)
print(response.status_code)
print(response.text)  # Mostra o conteúdo bruto da resposta

