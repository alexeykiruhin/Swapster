from django.urls import path

from .views import *

app_name = 'swaps'
urlpatterns = [
    path('', SwapIndex.as_view(), name='index'),
    path('detail/<int:swap_id>/', SwapDetail.as_view(), name='detail'),
    path('add_swap/<int:id>', add_swap, name='add_swap'),
    path('add_swap2/<int:swap_id>/<int:lot_id>', add_swap2, name='add_swap2'),
]
