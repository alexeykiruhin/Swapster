from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from ..Lots.models import Lot
from .models import Swap


def index(request):
    latest_swaps_list = Swap.objects.order_by('-swap_date')
    return render(request, 'swaps/list.html', {'latest_swaps_list': latest_swaps_list})


def detail(request, swap_id):
    try:
        swap = Swap.objects.get( id = swap_id )
        # список пользовательских лотов
        latest_lots_list = Lot.objects.filter(usernew_id=request.user.id).order_by('-lot_date')

    except:
        raise Http404('Свап не найден')

    return render(request, 'swaps/detail.html', {'swap': swap, 'latest_lots_list': latest_lots_list})



def add_swap(request, id=0):
    # надо выдернуть количество свапов в бд и добавлять в название
    latest_swaps_list = Swap.objects.all()
    count = len(latest_swaps_list)+1

    # создание свапа
    # берем айди лота для создания свапа

    s = Swap(swap_title=f'Swap_#{count}', id_lot_1=id, id_lot_2='null', swap_date=timezone.now())
    s.save(force_insert=True)
    return HttpResponseRedirect(reverse('swaps:index'))


def add_swap2(request, swap_id, lot_id):
    # поиск свапа в бд по айди
    swap = Swap.objects.get(id=swap_id)
    # присваиваем айди 2 лота в свап
    swap.id_lot_2 = lot_id
    swap.save()
    return HttpResponseRedirect(reverse('swaps:index'))
