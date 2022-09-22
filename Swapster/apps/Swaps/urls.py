from django.urls import path

from . import views

app_name = 'swaps'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:swap_id>/', views.detail, name='detail'),
    path('add_swap/<int:id>', views.add_swap, name='add_swap'),
    path('add_swap2', views.add_swap2, name='add_swap2'),
]
