import datetime
import requests
from django.shortcuts import render
import os
from .models import WeatherSearch


api_key = os.getenv("WEATHER_API_KEY")


def home(request):

    current_weather_url = (
        "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"
    )
    forecast_url = (
        "https://api.openweathermap.org/data/2.5/forecast?q={}&appid={}&units=metric"
    )

    weather_data = None
    forecast_data = None
    error = None
    if request.method == "POST":
        city = request.POST.get("city", "").strip()
        if city:
            weather_data, forecast_data = weather_and_forecast(
                city, api_key, current_weather_url, forecast_url
            )
            if not weather_data:
                error = "City Not Found"
            else:
                WeatherSearch.objects.create(
                    city=weather_data["city"], temperature=weather_data["temperature"]
                )

        else:
            error = "Please enter a city name"

    context = {
        "weather_data": weather_data,
        "forecast_data": forecast_data,
        "error": error,
    }

    return render(request, "home.html", context)


def weather_and_forecast(city, api_key, current_weather_url, forecast_url):

    weather_response = requests.get(current_weather_url.format(city, api_key)).json()
    # print("Weather Response:", weather_response)
    if str(weather_response.get("cod")) != "200":
        return None, None

    forecast_response = requests.get(forecast_url.format(city, api_key)).json()
    # print("Forecast Response:", forecast_response)
    if str(forecast_response.get("cod")) != "200":
        return None, None

    weather_data = {
        "city": city,
        "temperature": round(weather_response["main"]["temp"], 2),
        "description": weather_response["weather"][0]["description"],
        "icon": weather_response["weather"][0]["icon"],
    }
    forecast_data = []
    for daily_data in forecast_response["list"][::8][:5]:
        forecast_data.append(
            {
                "day": datetime.datetime.fromtimestamp(daily_data["dt"]).strftime("%A"),
                "temperature": round(daily_data["main"]["temp"], 2),
                "description": daily_data["weather"][0]["description"],
                "icon": daily_data["weather"][0]["icon"],
            }
        )

    return weather_data, forecast_data
