from django.db import models
from doctors.models import Doctor
from pets.models import Pet
from clients.models import Client


class WorkingSlot(models.Model):
    doctor = models.ForeignKey(
                            Doctor,
                            on_delete=models.CASCADE,
                            verbose_name='Врач',
                            related_name='working_slots')
    date = models.DateField('Дата приема')
    start = models.TimeField('Начало приема')
    end = models.TimeField('Окончание приема')
    is_available = models.BooleanField('Доступность для записи', default=True)

    class Meta:
        verbose_name = 'Окно приема'
        verbose_name_plural = 'Окна приема'

    def __str__(self):
        return f"{self.doctor} — {self.date.strftime('%d.%m.%Y')} ({self.start.strftime('%H:%M')} - {self.end.strftime('%H:%M')})"

class Booking(models.Model):
    slot = models.ForeignKey(
                        WorkingSlot,
                        on_delete=models.CASCADE,
                        verbose_name='Визит')
    pet = models.ForeignKey(
                        Pet,
                        on_delete=models.CASCADE,
                        verbose_name='Питомец',
                        related_name='pet_bookings')
    client = models.ForeignKey(
                        Client,
                        on_delete=models.CASCADE,
                        verbose_name='Клиент',
                        related_name='client_bookings')

    class Statuses(models.TextChoices):
        SCHEDULED = "scheduled", "Ожидается"
        COMPLETED = "completed", "Завершен"
        CANCELED = "canceled", "Отменен"
        NO_SHOW = "no_show", "Пациент не явился"
    
    status = models.CharField('Статус визита', 
                              max_length=20, 
                              choices=Statuses.choices, 
                              default=Statuses.SCHEDULED)

    class Meta:
                verbose_name = 'Бронь записи'
                verbose_name_plural = 'Брони записей'


class MedicalHistory(models.Model):
    pet = models.ForeignKey(
                            Pet,
                            on_delete=models.CASCADE,
                            verbose_name='Питомец',
                            related_name='history')
    visit = models.OneToOneField(
                            Booking,
                            on_delete=models.CASCADE,
                            verbose_name='Визит',
                            related_name='history')
    complaints = models.TextField('Жалобы', default='Плановый осмотр')
    diagnosis = models.TextField('Диагноз', default='Здоровье впорядке')
    prescription  = models.TextField('Назначения', null=True)
    next_visit  = models.CharField('Повторный прием', max_length=250, default='Не требуется')

    class Meta:
                verbose_name = 'История посещений'
                verbose_name_plural = 'Истории посещений'
    