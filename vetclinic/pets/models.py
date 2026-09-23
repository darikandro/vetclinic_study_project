from django.db import models
from clients.models import Client


GENDER = {
    "F": "женский",
    "M": "мужской"
}

ANIMAL_TYPE = {
    "cat": "кошка",
    "dog": "собака"
}

class Pet(models.Model):
    name = models.CharField("Кличка", max_length=60)
    type = models.CharField("Вид", max_length=3, choices=ANIMAL_TYPE)
    breed = models.CharField("Порода", max_length=60)
    gender = models.CharField("Пол", max_length=1, choices=GENDER)
    photo = models.ImageField("Фото", upload_to="pets/", blank=True, null=True)
    birth_date = models.DateField("Дата рождения", null=True)
    owner = models.ForeignKey(
                        Client,
                        on_delete=models.CASCADE,
                        verbose_name="Владелец",
                        related_name="pets")

    class Meta:
            verbose_name = "Питомец"
            verbose_name_plural = "Питомцы"
    
    def __str__(self):     
        return self.name