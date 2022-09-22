from django.contrib import admin

from ..Lots.models import Lot

from .models import Swap

admin.site.register(Swap)
admin.site.register(Lot)
