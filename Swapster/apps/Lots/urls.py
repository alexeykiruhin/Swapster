from django.urls import path

from .views import *

app_name = 'lots'
urlpatterns = [
    path('', LotIndex.as_view(), name='index'),
    path('<int:lot_id>/', LotDetail.as_view(), name='detail'),
    path('add_lot/', add_lot, name='add_lot'),
]
