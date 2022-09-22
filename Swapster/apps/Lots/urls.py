from django.urls import path

from . import views
from ..Swaps import views as vi

app_name = 'lots'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:lot_id>/', views.detail, name='detail'),
    path('add_lot/', views.add_lot, name='add_lot'),
]
