import requests

def getCityDetails(apiKey):
  API_KEY = apiKey

  city = "Dhaka"

  url = "https://api.openweathermap.org/data/2.5/weather"

  params = {
      "q": city,
      "appid": API_KEY,
      "units": "metric"
  }

  response = requests.get(url, params=params)

  data = response.json()

  if response.status_code == 200:
      temp = data["main"]["temp"]
      weather = data["weather"][0]["description"]

      print(f"City: {city}")
      print(f"Temperature: {temp}°C")
      print(f"Weather: {weather}")
      
      value = f"In {city}, Temprature is {temp}°C and Weather seams like {weather}"
      return value

  else:
      print("Error:", data["message"])