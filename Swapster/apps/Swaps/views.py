from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from ..Lots.models import Lot
from .models import Swap


def index(request):
    latest_swaps_list = Swap.objects.order_by('-swap_date')[:5]
    return render(request, 'swaps/list.html', {'latest_swaps_list': latest_swaps_list})


def detail(request, swap_id):
    try:
        s = Swap.objects.get( id = swap_id )
        latest_lots_list = Lot.objects.order_by('-lot_date')[0].id
        print(latest_lots_list)
    except:
        raise Http404('Свап не найден')

    return render(request, 'swaps/detail.html', {'swap': s, 'lot_id': latest_lots_list})



def add_swap(request, id=1):
    # надо выдернуть количество свапов в бд и добавлять в название
    latest_swaps_list = Swap.objects.all()
    count = len(latest_swaps_list)+1

    s = Swap(swap_title=f'Swap_#{count}', id_lot_1=id, id_lot_2=1, swap_date=timezone.now())
    s.save(force_insert=True)
    print('ГОтвово')
    return HttpResponseRedirect(reverse('swaps:index'))


def add_swap2(request):
    pass
    return HttpResponseRedirect(reverse('swaps:index'))