import telebot
import requests
from bs4 import BeautifulSoup as bs
from datetime import date
import schedule
bot = telebot.TeleBot("6206868826:AAG8FsOoZf1aEJamlRRhtIvt2Ye_csT5BAo", parse_mode='HTML')

@bot.message_handler(commands = ["weather"])
def weather(message):
    req = requests.get('https://yandex.ru/pogoda/moscow/details/10-day-weather/')
    html = bs(req.content, "lxml")
    temperature = []
    for i in html.find_all('span', class_="temp__value temp__value_with-unit", limit=12):
        temperature.append(i.text)

    type_condition = []
    for i in html.find_all('td', class_="weather-table__body-cell weather-table__body-cell_type_condition", limit=4):
        type_condition.append(i.text)

    air_pressure = []
    for i in html.find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_air-pressure', limit=4):
        air_pressure.append(i.text)

    humidity = []
    for i in html.find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_humidity'):
        humidity.append(i.text)

    wind_speed = []
    for i in html.find_all('span', class_="wind-speed", limit=4):
        wind_speed.append(i.text)

    UV_index = html.find('dd', class_="forecast-fields__value forecast-fields__value_red").text
    #print(UV_index)

    wd = date.today().weekday()
    #print(wd)
    week_day = [
        'Понедельник',
        'Вторник',
        'Среда',
        'Черверг',
        'Пятница',
        'Суббота',
        'Воскресенье'
    ][wd]
    date_today = date.today().strftime('%d.%m.%y')
    display_weather = str(date_today) + ' ' + week_day +'\n'

    time_of_day = [
        'Утро',
        'День',
        'Вечер',
        'Ночь'
    ]
    #print(type(time_of_day[0]))

    for i in range(4):
        display_weather += \
            time_of_day[i] + '\n' + \
            '   От ' + temperature[3*i] + ' до ' + temperature[3*i+1] + \
            ', ощущается как ' + temperature[3*i+2] + ', ' + type_condition[i] + '\n' + \
            "   Влажность: " + humidity[i] + '\n' + \
            "   Скорость ветра: " + wind_speed[i] + '\n' + \
            "   Давление: " + air_pressure[i] + '\n'

    #print(display_weather)




    bot.send_message(message.chat.id, display_weather)

bot.polling(non_stop=True)