from typing import Any, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionAskCategories(Action):
    def name(self) -> str:
        return "action_ask_category"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:

        categories = ["Nails", "Massage", "Skincare"]
        images = ["https://i.imgur.com/AqDBFFB.jpeg",
                  "https://i.imgur.com/AqDBFFB.jpeg",
                  "https://i.imgur.com/HfwExi7.jpeg"]
        buttons = [
            {"title": category, "payload": f"{category}"}
            for category in categories
        ]

        dispatcher.utter_message(
            text="Please choose a category:",
            buttons=buttons
        )
        return []
