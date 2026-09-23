from django.db import models


class Specialty(models.Model):
    name = models.CharField("Название специальности", max_length=60)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Специальность"
        verbose_name_plural = "Специальности"


class Doctor(models.Model):
    name = models.CharField("Имя", max_length=30)
    surname = models.CharField("Фамилия", max_length=60)
    patronymic = models.CharField("Отчество", max_length=30, blank=True, default="")
    specialty = models.ManyToManyField(Specialty, related_name="doctors")
    photo = models.ImageField(upload_to='doctors/', blank=True, null=True)

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"

    def __str__(self):
        if self.patronymic:
            str_result = f"{self.surname} {self.name[0]}. {self.patronymic[0]}."
        else:
            str_result = f"{self.surname} {self.name[0]}."

        return str_result
    
    def full_name(self):
        if self.patronymic:
            return f"{self.surname} {self.name} {self.patronymic}"
        else:
            return f"{self.surname} {self.name}"
