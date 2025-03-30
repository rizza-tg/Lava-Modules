# meta developer: @LavaModules

from .. import loader, utils
import aiohttp

@loader.tds
class WeatherMod(loader.Module):
    """Модуль для просмотра погоды"""

    strings = {
        "name": "L:Weather",
        "no_city": "<b>[☁️] - Укажите город!</b>",
        "error": "<b>[☁️] - Ошибка получения погоды.</b>",
        "weather": (
            "<b>[☁️] - Погода в {}</b>\n\n"
            "<b>• [🫟] Состояние: {}</b>\n"
            "<b>• [🫟] Температура: {}°C</b>\n"
            "<b>• [🫟] Ветер: {} км/ч</b>\n"
            "<b>• [🫟] Влажность: {}%</b>"
        )
    }

    async def weathercmd(self, message):
        """Использование: .weather <город>"""
        args = utils.get_args_raw(message)
        
        if not args:
            await utils.answer(message, self.strings["no_city"])
            return

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"https://wttr.in/{args}?format=j1&lang=ru",
                    headers={"User-Agent": "curl/7.68.0"}
                ) as response:
                    if response.status != 200:
                        await utils.answer(message, self.strings["error"])
                        return
                    
                    weather_data = await response.json()
                    current = weather_data["current_condition"][0]
                    
                    await utils.answer(
                        message,
                        self.strings["weather"].format(
                            args,
                            current["lang_ru"][0]["value"],
                            current["temp_C"],
                            current["windspeedKmph"],
                            current["humidity"]
                        )
                    )
            except Exception as e:
                await utils.answer(message, self.strings["error"])
