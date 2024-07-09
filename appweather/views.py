import os
import requests
import json
from django.shortcuts import render, HttpResponse
from django.http import HttpResponseBadRequest

SECRET_API_KEY = os.environ.get("SECRET_API_KEY")
URL_REQUEST_WEATHER = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'
URL_REQUEST_ICON = 'https://openweathermap.org/img/wn/{}.png'

if not SECRET_API_KEY:
    print("Установите 'SECRET_API_KEY' для корректного поведения")

def index(request):
    return render(request, 'appweather/index.html')


def get_weather(request):
    if request.method == "POST":
        city = request.POST.get('name_city')

        try:
            result = requests.get(URL_REQUEST_WEATHER.format(city, SECRET_API_KEY))
        except Exception as e:
            print(e, end='\n')
            print("Вы не установили SECRET_API_KEY в свою VENV")
            return HttpResponseBadRequest("<h1>Error 400 - Bad Request</h1>")
        
        response_js = json.loads(result.text)
        weather = response_js.get('weather')[0].get('main')
        temp = response_js.get('main').get('temp')
        pressure = response_js.get('main').get('pressure')
        humidity = response_js.get('main').get('humidity')
        wind_speed = response_js.get('wind').get('speed')
        icon = response_js.get('weather')[0].get('icon')

        # get url icon
        url_icon = URL_REQUEST_ICON.format(icon)

        context = {
            'title': 'Get Weather',
            'city': city,
            'weather': weather,
            'temp': temp,
            'pressure': int(pressure) * 0.75,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'url_icon': url_icon,
        }
        
        return render(request, 'appweather/get_weather.html', context=context)

    else:
        context = {
            'title': 'Get Weather',
        }

        return render(request, 'appweather/get_weather.html', context=context)
