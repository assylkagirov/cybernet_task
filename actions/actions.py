from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionProcessSuccess(Action):
    def name(self) -> Text:
        return "action_process_success"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        iin = tracker.get_slot('iin')
        dispatcher.utter_message(text=f"Ваш ИИН подтвержден: {iin}. Спасибо!")
        return []

class ActionHandleIncorrectIIN(Action):
    def name(self) -> Text:
        return "action_handle_incorrect_iin"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        iin = tracker.get_slot('iin')
        if iin and len(iin) == 12:
            dispatcher.utter_message(
                text=f"Хорошо, давайте проверим ваш ИИН частями. Первые 6 цифр: «{iin[:6]}». "
                     f"Остальные 6 цифр: «{iin[6:]}». Всё верно?"
            )
        else:
            dispatcher.utter_message(text="Пожалуйста, введите ИИН из 12 цифр.")
        return []

class ActionCheckFirstSixDigits(Action):
    def name(self) -> Text:
        return "action_check_first_six_digits"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        first_six_digits = tracker.get_slot('first_six_digits')
        if first_six_digits:
            dispatcher.utter_message(text=f"Первые 6 цифр: «{first_six_digits}». Всё верно?")
        else:
            dispatcher.utter_message(text="Пожалуйста, продиктуйте первые 6 цифр в формате '12-34-56'.")
        return []

class ActionCheckLastSixDigits(Action):
    def name(self) -> Text:
        return "action_check_last_six_digits"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        last_six_digits = tracker.get_slot('last_six_digits')
        if last_six_digits:
            dispatcher.utter_message(text=f"Остальные 6 цифр: «{last_six_digits}». Всё верно?")
        else:
            dispatcher.utter_message(text="Пожалуйста, продиктуйте последние 6 цифр в формате '12-34-56'.")
        return []
