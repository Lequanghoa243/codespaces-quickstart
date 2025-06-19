from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from db.store_db_connect import db

class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"
    def convert_minutes_to_time(self, minutes: int) -> str:
        """Convert minutes into 'HhMM' format."""
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours}h" if mins == 0 else f"{hours}h{mins}"

    def get_working_hours(self) -> str:
        """Fetch and format business working hours with grouped days."""
        day_abbr_map = {
            "mo": "Mon", "tu": "Tue", "we": "Wed",
            "th": "Thu", "fr": "Fri", "sa": "Sat", "su": "Sun"
        }

        result = db.run("SELECT * FROM business_work_day LIMIT 1;", fetch="cursor", include_columns=True)
        columns = result.keys()
        row = result.fetchone()

        if not row:
            return "No working hours found."

        row_data = dict(zip(columns, row))

        # Build a dict: day -> time range string
        schedule = {}
        for abbr, label in day_abbr_map.items():
            if abbr in row_data and row_data[abbr]:
                times = list(map(int, row_data[abbr].split(',')))
                if len(times) == 2:
                    open_time = self.convert_minutes_to_time(times[0])
                    close_time = self.convert_minutes_to_time(times[1])
                    schedule[label] = f"{open_time} - {close_time}"

        # Reverse: group days with the same time
        reverse_schedule = {}
        for day, time_range in schedule.items():
            reverse_schedule.setdefault(time_range, []).append(day)

        # Format output
        description = ""
        for time_range, days in reverse_schedule.items():
            if len(days) == 1:
                description += f"{days[0]}: {time_range}\n"
            else:
                description += f"{days[0]} to {days[-1]}: {time_range}\n"

        return description.strip()

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        result = db.run("SELECT name, address, phone FROM business;", fetch="cursor", include_columns=True)
        row = result.fetchone()

        working_hours = self.get_working_hours()
        dispatcher.utter_message(
            text=(
                f"👋 Welcome to **{row[0]}**!\n"
                f"📍 **Address:** {row[1]}\n"
                f"📞 **Phone:** {row[2]}\n"
                f"🕘 **Working Hours:**\n{working_hours}\n\n"
                f"I'm **DigiAI**, your smart assistant. I can help you *book appointments* or explore our services."
                f"What would you like to do?"
            ),
            buttons=[
                {"title": "💅 Book Appointment", "payload": "Book Appointment"},
                {"title": "📋 Explore Services", "payload": "Explore Services"},
            ]
        )
        return []
