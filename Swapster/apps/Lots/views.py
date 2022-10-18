from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView

from .models import Lot
from ..Swaps.models import Swap
from django.db.models import Q


class LotIndex(ListView):
    model = Lot
    template_name = 'lots/list.html'
    # context_object_name = 'my_lots_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Лоты'
        context['my_lots_list'] = self.model.objects.filter(usernew_id=self.request.user.id)\
            .order_by('-lot_date')\
            .exclude(in_swap=True)
        context['lots_in_swap_list'] = self.model.objects.filter(usernew_id=self.request.user.id, in_swap=True)\
            .order_by('-lot_date')
        context['my_swaps_list'] = Swap.objects.filter(Q(lot_1__usernew_id=self.request.user.id) |
                                                             Q(lot_2__usernew_id=self.request.user.id))
        return context

    # def get_queryset(self):
    #    # допустим тут выбираем только лоты этого юзера а в гет контекст дата уже делаем фильтры
    #    return Lot.objects.filter(usernew_id=self.request.user.id).order_by('-lot_date').exclude(in_swap=True)

#def index(request):
#    if request.user.is_anonymous:
#        return HttpResponseRedirect(reverse('swaps:index'))
#    else:
#        # список моих лотов их надо разделить на те которые уже в свапе и которые нет
#        my_lots_list = Lot.objects.filter(usernew_id=request.user.id).order_by('-lot_date').exclude(in_swap=True)
#        # лоты которые участвуют в свапах
#        lots_in_swap_list = Lot.objects.filter(usernew_id=request.user.id, in_swap=True).order_by('-lot_date')
#        # ищем свои свапы по первому лоту и второму лоту
#        my_swaps_list = Swap.objects.filter(Q(lot_1__usernew_id=request.user.id) | Q(lot_2__usernew_id=request.user.id))
#        return render(request, 'lots/list.html', {'my_lots_list': my_lots_list,
#                                                  'my_swaps_list': my_swaps_list,
#                                                  'lots_in_swap_list': lots_in_swap_list})


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
