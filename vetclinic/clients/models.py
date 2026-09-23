from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Client(models.Model):
    surname = models.CharField("Фамилия", max_length=64, db_index=True)
    name = models.CharField("Имя", max_length=30)
    patronymic = models.CharField("Отчество", max_length=30, blank=True, default="")
    phone_number = PhoneNumberField("Номер телефона", unique=True, db_index=True)
    email = models.EmailField("Электронная почта", blank=True, null=True)
    user_profile = models.OneToOneField(
        User, 
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
        verbose_name="Пользователь сайта",
        related_name="client_profile")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
            if self.patronymic:
                str_result = f"{self.surname} {self.name} {self.patronymic}"
            else:
                str_result = f"{self.surname} {self.name}"
    
            return str_result