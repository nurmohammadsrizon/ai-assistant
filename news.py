import requests

def getnews(apiKey):
  api_key = apiKey

  url = "https://newsapi.org/v2/top-headlines"

  params = {
      "country": "us",
      "apiKey": api_key
  }

  response = requests.get(url, params=params)
  data = response.json()

  for article in data["articles"]:
      return article["title"]