from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import Lot
from django.contrib.auth.models import User


def index(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('swaps:index'))
    else:
        latest_lots_list = Lot.objects.filter(usernew_id=request.user.id)
        return render(request, 'lots/list.html', {'latest_lots_list': latest_lots_list})


def detail(request, lot_id):
    try:
        lot = Lot.objects.get( id = lot_id )
    except:
        raise Http404('Лот не найден')
    # проверяем чей лот, если этого юзера то показываем
    if lot.usernew_id == request.user.id:
        return render(request, 'lots/detail.html', {'lot': lot})
    else:
        raise Http404('Лот не найден')


def add_lot(request):
    o = Lot(lot_title=request.POST['title'], lot_text=request.POST['text'], lot_date=timezone.now(), usernew_id=request.user.id)
    print(request.user.id)
    o.save(force_insert=True)
    return HttpResponseRedirect(reverse('lots:index'))



