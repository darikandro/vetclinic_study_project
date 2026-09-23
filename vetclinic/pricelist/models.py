from django.db import models


class ServiceCategory(models.Model):
    name = models.CharField("Категория", max_length=64)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Категория услуг"
        verbose_name_plural = "Категории услуг"


class Service(models.Model):
    name = models.CharField("Услуга", max_length=128)
    category = models.ForeignKey(
        ServiceCategory, 
        on_delete=models.PROTECT, 
        default=None, 
        null=True, 
        verbose_name="Категория"
    )
    price = models.FloatField("Цена, BYN")
    comment = models.CharField("Комментарий", max_length=256, default='', blank=True)

    def __str__(self):
        return f" {self.name} {self.price} BYN"
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
