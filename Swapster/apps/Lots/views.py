from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import Lot
from ..Swaps.models import Swap


def index(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('swaps:index'))
    else:
        latest_lots_list = Lot.objects.filter(usernew_id=request.user.id).order_by('-lot_date')
        # ищем свои свапы по первому лоту
        my_swaps_in_lot_1 = Swap.objects.filter(lot_1__usernew_id=request.user.id)
        # ищем свои свапы по второму лоту и добавляем к списку из первх лотов
        my_swaps_in_lot_2 = Swap.objects.filter(lot_2__usernew_id=request.user.id)
        # список айди моих свапов
        swaps_id = []

        for swap in my_swaps_in_lot_1:
            swaps_id.append(swap.id)

        for swap in my_swaps_in_lot_2:
            swaps_id.append(swap.id)

        # список экземпляров объектов моих слотов
        list_my_swaps = Swap.objects.filter(id__in=swaps_id)
        return render(request, 'lots/list.html', {'latest_lots_list': latest_lots_list, 'list_my_swaps': list_my_swaps})


def detail(request, lot_id):
    # проверяем есть ли такой лот
    try:
        lot = Lot.objects.get(id=lot_id)
    except:
        raise Http404('Лот не найден')
    # проверяем чей лот, если этого юзера то показываем
    if lot.usernew_id == request.user.id:
        return render(request, 'lots/detail.html', {'lot': lot})
    else:
        raise Http404('Лот не найден')


def add_lot(request):
    o = Lot(lot_title=request.POST['title'], lot_text=request.POST['text'],
            lot_date=timezone.now(), usernew_id=request.user.id)
    print(request.user.pk)
    o.save(force_insert=True)
    return HttpResponseRedirect(reverse('lots:index'))
