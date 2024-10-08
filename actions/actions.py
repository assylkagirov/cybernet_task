from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionHandleIncorrectIIN(Action):
    def name(self) -> Text:
        return "action_handle_incorrect_iin"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        iin = tracker.get_slot('iin')

        first_six = iin[:6]
        last_six = iin[6:]
        dispatcher.utter_message(text=f"Первые 6 цифр вашего ИИН: {first_six}")

        if iin and len(iin.replace(" ", "")) == 12:
            first_six = iin[:6]
            last_six = iin[6:]
            
            # Убедимся, что слоты заполнены
            if first_six and last_six:
                dispatcher.utter_message(
                    text=f"Ваш ИИН: {iin}. Давайте проверим первые 6 цифр: {first_six}. Всё верно?"
                )
                return [
                    SlotSet("first_six_digits", first_six),
                    SlotSet("last_six_digits", last_six),
                    SlotSet("step_state", "first_six_confirmation")
                ]
            else:
                dispatcher.utter_message(text="Произошла ошибка при разделении ИИН. Попробуйте снова.")
        else:
            dispatcher.utter_message(text="ИИН должен содержать 12 цифр. Пожалуйста, введите корректный ИИН.")
        return []


class ActionCheckFirstSixDigits(Action):
    def name(self) -> Text:
        return "action_check_first_six_digits"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        last_intent = tracker.latest_message['intent'].get('name')
        first_six_digits = tracker.get_slot('first_six_digits')
        step_state = tracker.get_slot("step_state")

        if not first_six_digits:
            dispatcher.utter_message(text="Первые 6 цифр не найдены. Пожалуйста, введите ИИН заново.")
            return [SlotSet("step_state", "first_six_entry")]

        if last_intent == "affirm" and step_state == "first_six_confirmation":
            dispatcher.utter_message(text="Хорошо, теперь давайте проверим последние 6 цифр.")
            return [SlotSet("step_state", "last_six_confirmation")]

        elif last_intent == "deny" and step_state == "first_six_confirmation":
            dispatcher.utter_message(text="Пожалуйста, введите новые первые 6 цифр.")
            return [SlotSet("step_state", "first_six_entry")]

        return []


class ActionCheckLastSixDigits(Action):
    def name(self) -> Text:
        return "action_check_last_six_digits"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        last_intent = tracker.latest_message['intent'].get('name')
        last_six_digits = tracker.get_slot('last_six_digits')
        step_state = tracker.get_slot("step_state")

        if not last_six_digits:
            dispatcher.utter_message(text="Последние 6 цифр не найдены. Пожалуйста, введите ИИН заново.")
            return [SlotSet("step_state", "last_six_entry")]

        if last_intent == "affirm" and step_state == "last_six_confirmation":
            dispatcher.utter_message(text="ИИН полностью подтверждён. Спасибо!")
            return [SlotSet("step_state", "iin_confirmation")]

        elif last_intent == "deny" and step_state == "last_six_confirmation":
            dispatcher.utter_message(text="Пожалуйста, введите новые последние 6 цифр.")
            return [SlotSet("step_state", "last_six_entry")]

        return []
