from typing import Any, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionAskServices(Action):
    def name(self) -> str:
        return "action_ask_service"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:

        category = tracker.get_slot("category")
        services_by_category = {
            "Nails": ["Manicure", "Pedicure", "Gel Nails"],
            "Massage": ["Swedish", "Deep Tissue", "Hot Stone"],
            "Skincare": ["Facial", "Acne Treatment"]
        }

        services = services_by_category.get(category, [])

        if services:
            buttons = [{"title": service, "payload": f"{service}"} for service in services]
            dispatcher.utter_message(
                text=f"Here are the services under *{category}*. Please choose one:",
                buttons=buttons
            )
        else:
            dispatcher.utter_message(
                text=f"Sorry, I couldn't find services under '{category}'. Please try again."
            )

        return []
