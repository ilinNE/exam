import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .utils import get_nearest_birthday_employee, serialize_employee_nearest_payload


class BirthdayConsumer(WebsocketConsumer):
    group_name = "birthdays"

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

        nearest = get_nearest_birthday_employee()
        if nearest is None:
            payload = {"username": None, "birth_date": None, "days_until": None}
        else:
            user, days = nearest
            payload = serialize_employee_nearest_payload(user, days)

        self.send(text_data=json.dumps({"type": "initial", "data": payload}))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )

    def birthdays_update(self, event):
        data = event.get("data")
        self.send(text_data=json.dumps({"type": "update", "data": data}))
