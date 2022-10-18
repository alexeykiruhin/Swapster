from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView

from ..Lots.models import Lot
from .models import Swap
from django.db.models import Q


class SwapIndex(ListView):
    model = Swap
    template_name = 'swaps/list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Свапы'
        # анонимному пользователю показываем все свапы(за исключением полных с 2мя лотами)
        if self.request.user.is_anonymous:
            context['all_swaps_list'] = Swap.objects.order_by('-swap_date').exclude(swap_full=True)
        else:
            # убираем свапы пользователя из общего списка показываемого ему же
            context['exclude_my_swaps_list'] = self.model.objects.exclude(Q(lot_1__usernew_id=self.request.user.id) |
                                                     Q(lot_2__usernew_id=self.request.user.id)).exclude(swap_full=True)
        return context


class SwapDetail(DetailView):
    model = Swap
    template_name = 'swaps/detail.html'
    pk_url_kwarg = 'swap_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # добавить условие отображения свапов, если он фулл то не показываем лоты для добавления,
        # так же если свап фуловый то надо его пометить в списке мои свапы(т.е. есть предложение на обмен)
        context['swap'] = self.object
        # список пользовательских лотов не участвующих в свапах
        context['my_lots_list'] = Lot.objects.filter(usernew_id=self.request.user.id).order_by('-lot_date')\
                                                                                     .exclude(in_swap=True)
        return context


def add_swap(request, id=0):
    # надо выдернуть количество свапов в бд и добавлять в название
    # убрать в последствии
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
