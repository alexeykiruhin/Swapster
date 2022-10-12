from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from ..Lots.models import Lot
from .models import Swap
from django.db.models import Q


def index(request):
    # анонимному пользователю показываем все свапы(за исключением полных с 2мя лотами)
    if request.user.is_anonymous:
        latest_swaps_list = Swap.objects.order_by('-swap_date').exclude(swap_full=True)
        return render(request, 'swaps/list.html', {'latest_swaps_list': latest_swaps_list})
    else:
        # убрать свапы с твоими лотами из общего списка, они показываются только на странице с твоими свапами
        # ищем свои свапы по первому лоту и второму лоту
        # список экземпляров объектов моих слотов, которые надо ИСКЛЮЧИТЬ из общего списка свапов
        list_exclude_my_swaps = Swap.objects.exclude(Q(lot_1__usernew_id=request.user.id) |
                                                     Q(lot_2__usernew_id=request.user.id)).exclude(swap_full=True)
        # название списка передаваемого во вью такое же как и для анонимного пользователя
        return render(request, 'swaps/list.html', {'latest_swaps_list': list_exclude_my_swaps})


def detail(request, swap_id):
    # добавить условие отображения свапов, если он фулл то не показываем лоты для добавления,
    # так же если свап фуловый то надо его пометить(т.е. есть предложение на обмен)
    try:
        swap = Swap.objects.get(id=swap_id)
        # список пользовательских лотов не участвующих в свапах
        latest_lots_list = Lot.objects.filter(usernew_id=request.user.id).order_by('-lot_date').exclude(in_swap=True)
    except:
        raise Http404('Свап не найден')

    return render(request, 'swaps/detail.html', {'swap': swap, 'latest_lots_list': latest_lots_list})


def add_swap(request, id=0):
    # надо выдернуть количество свапов в бд и добавлять в название
    latest_swaps_list = Swap.objects.all()
    count = len(latest_swaps_list)+1
    # создание свапа
    # берем айди лота для создания свапа, айди второго лота пустое (null)
    s = Swap(swap_title=f'Swap_#{count}', lot_1_id=id, swap_date=timezone.now())
    s.save(force_insert=True)
    # в лоте который сюда передаём надо изменить поле in_swap на True
    lot = Lot.objects.get(id=id)
    lot.in_swap = True
    lot.save()
    return HttpResponseRedirect(reverse('swaps:index'))


def add_swap2(request, swap_id, lot_id):
    # поиск свапа в бд по айди
    swap = Swap.objects.get(id=swap_id)
    # присваиваем айди 2 лота в свап
    swap.lot_2_id = lot_id
    swap.swap_full = True
    swap.save()
    # в лоте который сюда передаём надо изменить поле in_swap на True
    lot = Lot.objects.get(id=lot_id)
    lot.in_swap = True
    lot.save()
    return HttpResponseRedirect(reverse('swaps:index'))
