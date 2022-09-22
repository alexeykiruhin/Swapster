from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from ..Swaps.views import add_swap
from .models import Lot


def index(request):
    latest_lots_list = Lot.objects.order_by('-lot_date')
    print('ИНДЕКС')
    return render(request, 'lots/list.html', {'latest_lots_list': latest_lots_list})


def detail(request, lot_id):
    try:
        l = Lot.objects.get( id = lot_id )
    except:
        raise Http404('Лот не найден')

    return render(request, 'lots/detail.html', {'lot': l})


def add_lot(request):
    print(request)
    o = Lot(lot_title=request.POST['title'], lot_text=request.POST['text'], lot_date=timezone.now())
    o.save(force_insert=True)
    print('добавилось-'+ str(o.id))
    return HttpResponseRedirect(reverse('lots:index'))



