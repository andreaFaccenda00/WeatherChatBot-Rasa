from typing import Any, Text, Dict, List
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionGetWeather(Action):

    def name(self) -> Text:
        return "action_get_weather"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        city_slot = next(tracker.get_latest_entity_values("city"), None)
        city = tracker.get_slot("city") or city_slot

        if city:
            weather_data = self.get_weather(city)
            if weather_data and weather_data.get("cod") == 200:
                temp = weather_data["main"]["temp"]
                desc = weather_data["weather"][0]["description"]
                response = f"A {city} ci sono {temp}°C con {desc}."
            else:
                response = f"Mi dispiace, non riesco a ottenere il meteo per {city}."
        else:
            response = "Per favore, indicami una città."

        dispatcher.utter_message(text=response)
        return []

    @staticmethod
    def get_weather(city: str) -> Dict[Text, Any]:
        api_key = "b860996c1bf309c8b3f039f21d55d518"
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "units": "metric",
            "lang": "it",  # risposte meteo in italiano
            "appid": api_key
        }

        try:
            response = requests.get(base_url, params=params)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Errore durante la richiesta API: {e}")
            return None
