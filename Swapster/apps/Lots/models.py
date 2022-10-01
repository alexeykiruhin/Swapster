from django.db import models
from django.contrib.auth.models import User


class Lot(models.Model):
    user = models.CharField('user', max_length=50, null=True)
    usernew = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    lot_title = models.CharField('Название', max_length=50)
    lot_text = models.CharField('Описание', max_length=200)
    lot_date = models.DateTimeField('Дата создания')

    def __str__(self):
        return self.lot_title

    class Meta:
        verbose_name = 'Лот'
        verbose_name_plural = 'Лоты'
