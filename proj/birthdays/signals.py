from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Employee
from .utils import get_nearest_birthday_employee, serialize_employee_nearest_payload


@receiver(post_save, sender=Employee)
def on_employee_saved(sender, instance: Employee, **kwargs):
    _broadcast_nearest()


@receiver(post_delete, sender=Employee)
def on_employee_deleted(sender, instance: Employee, **kwargs):
    _broadcast_nearest()


def _broadcast_nearest() -> None:
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return

    nearest = get_nearest_birthday_employee()
    if nearest is None:
        data = {"employee_name": None, "birth_date": None, "days_until": None}
    else:
        employee, days = nearest
        data = serialize_employee_nearest_payload(employee, days)

    async_to_sync(channel_layer.group_send)(
        "birthdays",
        {"type": "birthdays.update", "data": data},
    )
