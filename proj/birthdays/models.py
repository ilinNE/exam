from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=128)
    birth_date = models.DateField(
        "Дата рождения", null=True, blank=True, help_text="Дата рождения"
    )

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return self.name
