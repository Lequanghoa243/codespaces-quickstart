from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType


class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(
            text="👋 Welcome to **Beauty Blossom Spa**!\nI'm **DigiAI**, your assistant. I can help you *book appointments* or *explore our services and store information*. What would you like to do?",
            buttons=[
                {"title": "💅 Book Appointment", "payload": "Book Appointment"},
                {"title": "📋 Explore Store", "payload": "Explore Store"},
            ]
        )
        return []
