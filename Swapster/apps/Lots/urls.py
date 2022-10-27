from django.urls import path

from .views import *

app_name = 'lots'
urlpatterns = [
    path('', LotIndex.as_view(), name='index'),
    path('<int:lot_id>/', LotDetail.as_view(), name='detail'),
    path('add_lot/', LotAdd.as_view(), name='add_lot'),
    path('change_lot/<int:pk>', LotChange.as_view(), name='change'),
    path('delete_lot/<int:pk>', LotDelete.as_view(), name='delete'),
]
