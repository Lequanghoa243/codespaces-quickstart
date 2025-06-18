from typing import Any, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionExloreStore(Action):
    def name(self) -> str:
        return "action_explore_store"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        message = """
    Sure! Here's what you need to know about Go Nails Spa:
    📍 We’re located at 14622 Memorial Dr.
    📞 You can reach us at (281) 372-6899.
    🕘 Our working hours are:
    Monday to Saturday: 9 AM – 7 PM
    Sunday: 10 AM – 6 PM
    Would you like to book an appointment?
    """
        dispatcher.utter_message(
            text=message,
        )
        return []
