from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from db.store_db_connect import db  # replace with your actual db instance

class ActionAskCategories(Action):
    def name(self) -> str:
        return "action_ask_category"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:

        result = db.run("""
            SELECT c.name 
            FROM category c
            WHERE c.status = 2 
                AND c.type = 'service' 
                AND c.priority >= 0
            ORDER BY c.priority
        """, fetch="cursor", include_columns=True)

        rows = result.fetchall()
        categories = [row[0] for row in rows] 

        if not categories:
            dispatcher.utter_message(text="Sorry, there are no available service categories right now.")
            return []

        buttons = [
            {"title": category, "payload": f"{category}"}
            for category in categories
        ]

        dispatcher.utter_message(
            text="What service category would you like to explore?",
            buttons=buttons
        )
        return []


class ActionValidateCategory(Action):
    def name(self) -> str:
        return "action_validate_category"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Fetch valid service categories from the database
        result = db.run("""
            SELECT c.name 
            FROM category c
            WHERE c.status = 2 
              AND c.type = 'service' 
              AND c.priority >= 0
            ORDER BY c.priority
        """, fetch="cursor", include_columns=True)

        rows = result.fetchall()
        valid_categories = [row[0] for row in rows]

        user_input = tracker.get_slot("category")
        print(f"User selected category: {user_input}")

        if user_input not in valid_categories:
            dispatcher.utter_message(text="That input is not valid. Please choose one of the available options.")
            return [SlotSet("category", None)]

        return []


class ActionAskServices(Action):
    def name(self) -> str:
        return "action_ask_service"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]) -> List[Dict[str, Any]]:

        category = tracker.get_slot("category")

        result = db.run(f"""
            SELECT 
            s.name 
            FROM service s
            JOIN category c ON s.category_id = c.id
            WHERE s.web_booking_visible = 1 
            AND s.status = 1 
            AND c.status = 2 
            AND c.type = 'service' 
            AND c.priority >= 0
            AND c.name = "{category}";
            """, fetch="cursor", include_columns=True)
        
        rows = result.fetchall()
        services = [row[0] for row in rows] 
        if services:
            buttons = [{"title": service, "payload": f"{service}"} for service in services]
            dispatcher.utter_message(
                text=f"Here are the services under *{category}*. what service are you in the mood for today?",
                buttons=buttons
            )

        return []

class ActionValidateService(Action):
    def name(self) -> str:
        return "action_validate_service"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        category = tracker.get_slot("category")
        
        result = db.run(f"""
            SELECT 
            s.name 
            FROM service s
            JOIN category c ON s.category_id = c.id
            WHERE s.web_booking_visible = 1 
            AND s.status = 1 
            AND c.status = 2 
            AND c.type = 'service' 
            AND c.priority >= 0
            AND c.name = {category};
            """, fetch="cursor", include_columns=True)
        
        rows = result.fetchall()
        valid_services = [row[0] for row in rows] 
        user_input = tracker.get_slot("service")

        if user_input not in valid_services:
            dispatcher.utter_message(text="That service is not valid. Please choose one of the options.")
            return [SlotSet("service", None)]
        return []