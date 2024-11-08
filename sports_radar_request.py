import requests

url = "https://api.sportradar.com/tennis/trial/v3/en/competitions.json?api_key=9dZjJeeRpKuD0wYUBN2Let6OEVUnw4OF8IQYD1nG"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.text)