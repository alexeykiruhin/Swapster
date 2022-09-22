from django.db import models
from Swapster.apps.Lots.models import Lot


class Swap(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.SET_NULL, blank=True, null=True)
    swap_title = models.CharField('Обмен', max_length=50)
    id_lot_1 = models.CharField('Лот_1', max_length=50)
    id_lot_2 = models.CharField('Лот_2', max_length=50)
    swap_date = models.DateTimeField('Дата обмена')

    def __str__(self):
        return self.swap_title

    class Meta:
        verbose_name = 'Свап'
        verbose_name_plural = 'Свапы'
