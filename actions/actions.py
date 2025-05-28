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

        # you might prefer to pull this from an entity or a slot
        city = tracker.latest_message.get("text")
        weather_data = self.get_weather(city)

        if weather_data and weather_data.get("main"):
            temp = weather_data["main"]["temp"]
            desc = weather_data["weather"][0]["description"]
            response = f"The weather in {city} is {temp}°C with {desc}."
        else:
            response = f"Sorry, I could not fetch the weather information for {city}."

        dispatcher.utter_message(text=response)
        return []

    @staticmethod
    def get_weather(city: str) -> Dict[Text, Any]:
        api_key = "b860996c1bf309c8b3f039f21d55d518"
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "units": "metric",    # gradi Celsius
            "appid": api_key
        }

        try:
            print(f"API Requested URL : {base_url}?{params}")
            response = requests.get(base_url, params=params)
            api_response = response.json()
            print(f"API Response : {api_response}")
            return api_response
        except requests.exceptions.RequestException as e:
            print(f"API Request Error : {e}")
            return None
