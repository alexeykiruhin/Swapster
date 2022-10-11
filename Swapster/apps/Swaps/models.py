from django.db import models
from Swapster.apps.Lots.models import Lot


class Swap(models.Model):
    swap_title = models.CharField('Обмен', max_length=50)
    lot_1 = models.ForeignKey(Lot, on_delete=models.SET_NULL, null=True, related_name='first_lot')
    lot_2 = models.ForeignKey(Lot, on_delete=models.SET_NULL, null=True, related_name='second_lot')
    swap_full = models.BooleanField(default=False)
    swap_date = models.DateTimeField('Дата обмена')

    def __str__(self):
        return self.swap_title

    class Meta:
        verbose_name = 'Свап'
        verbose_name_plural = 'Свапы'
