import requests

url = "https://panel.rapiwha.com/send_message.php"

querystring = {"apikey":"5HUI8SLWMWEQSE0NQTAE","number":"+6282131740469","text":"testing"}

response = requests.request("GET", url, params=querystring)

print(response.text)