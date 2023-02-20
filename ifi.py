# Погоду лучше забирать с гисметио так как на их сайте нет защиты от автоматизированых программ сбора данных как на яандексе 
# Когда ты делал запрос в яандекс из крипта ты получат в ответ html с капчей
# с гисметио может еще попорабовать подаставить разные даные из страницы (температура воды и тюд)

import requests
from bs4 import BeautifulSoup
import urllib.parse

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

url_find_location = 'https://www.gismeteo.ru/mq/search/{:s}/9/'
url_parse_location = 'https://www.gismeteo.ru/{:s}/now/'


def find_location(loc):
    url = url_find_location.format(urllib.parse.quote_plus(loc))
    response = requests.get(url, headers=headers)
    data = response.json()

    if not data:
        return None

    if len(data['data']) == 0:
        return None

    return data['data'][0]['url']


def get_html(location_url):
    url = url_parse_location.format(location_url)
    response = requests.get(url, headers=headers)
    html = response.text

    return html


# noinspection PyBroadException
def get_weather_now(text):
    location_url = find_location(text)

    if not location_url:
        print(f'Город "{text}" не найден. Скорее всего вы сделали опечатку')
        return


    soup = BeautifulSoup(html, 'html.parser')

    try:
        now_blck = soup.find('div', class_='now')
        temperature = now_blck.find(class_='unit unit_temperature_c').text
        wind = now_blck.find(class_='unit unit_wind_m_s').get_text(" ")
        pressure = now_blck.find(class_='unit unit_pressure_mm_hg_atm').get_text(" ")

        info = """Температура воздуха сейчас: {:s}
Ветер: {:s}
Давление: {:s}
        """.format(temperature, wind, pressure)

        print(info)
    except Exception as e:
        print('Город "{:s}" не найден. Скорее всего вы сделали опечатку'.format(text))


if __name__ == '__main__':
    text = input('Введи город, в котором хочешь узнать погоду: ')
    # text = 'москва'
    # find_location(text)
    get_weather_now(text)