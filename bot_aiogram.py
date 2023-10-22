from pprint import pprint

import requests
import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN_API = "6069666751:AAEEKSFHd9xQK5U3A27RrToLMTitdA66PhY"
API_WEATHER = "8ca2c51c38a7133da9bd098697e95c53"

bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.reply("*****Привіт хозаїн! Хотів би знати яка погода?*****\n"
                        "*****Так ти напиши назву міста!*****")


@dp.message_handler()
async def get_weather(message: types.Message):
    dict_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облочно \U00002601",
        "Rain": "Дождик \U00002614",
        "Drizzle": "Дождик \U00002614",
        "Thunderstorm": "Грозище \U000026A1",
        "Snow": "Снижок \U0001F328",
        "Mist": "Туманчик \U0001F32B",
    }

    try:
        result = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?lang=ua&q="
            f"{message.text}&appid={API_WEATHER}&units=metric"
        )
        data = result.json()
        pprint(data)
        city = data["name"]
        country = data["sys"]["country"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in dict_smile:
            wd = dict_smile[weather_description]
        else:
            wd = "Погледай на вулицю, яка там погода а то я не розумію!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = sunset - sunrise

        await message.reply(f"****{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}****\n"
                            f"Погодка у {city}!\n"
                            f"Страна: {country}\n "
                            f"Температурка: {cur_weather}C° {wd}\n"
                            f"Волога на дворі: {humidity}%\n"
                            f"Давлюшеа на дворі: {pressure} мм.рт.стовба\n"
                            f"Вітерець: {wind} метра у секунду\n"
                            f"Всхід сонця: {sunrise}!\n"
                            f"Сонечко спать лягає у: {sunset}!\n"
                            f"Тривалість лня: {length_of_the_day}!\n"
                            f"****Усього доброго!****")
    except:
        await message.reply("\U00002620\U00002620 Перевірте назву міста \U00002620\U00002620")


if __name__ == "__main__":
    executor.start_polling(dp)
