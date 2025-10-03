from django.apps import AppConfig


class BirthdaysConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "birthdays"
    verbose_name = "Дни рождения"

    def ready(self) -> None:
        # Импорт сигналов при старте приложения
        from . import signals  # noqa: F401

        return super().ready()
