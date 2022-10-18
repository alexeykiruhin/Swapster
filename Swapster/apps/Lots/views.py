from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView

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
        # список моих лотов которые не в свапах
        context['my_lots_list'] = self.model.objects.filter(usernew_id=self.request.user.id)\
            .order_by('-lot_date')\
            .exclude(in_swap=True)
        # список лотов которые в свапах
        context['lots_in_swap_list'] = self.model.objects.filter(usernew_id=self.request.user.id, in_swap=True)\
            .order_by('-lot_date')
        # список моих свапов
        context['my_swaps_list'] = Swap.objects.filter(Q(lot_1__usernew_id=self.request.user.id) |
                                                             Q(lot_2__usernew_id=self.request.user.id))
        return context

    # def get_queryset(self):
    #    # допустим тут выбираем только лоты этого юзера а в гет контекст дата уже делаем фильтры
    #    return Lot.objects.filter(usernew_id=self.request.user.id).order_by('-lot_date').exclude(in_swap=True)


class LotDetail(DetailView):
    model = Lot
    template_name = 'lots/detail.html'
    # slug_url_kwarg = 'lot_slug'
    pk_url_kwarg = 'lot_id'
    # context_object_name = 'lot'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # проверяем чей лот, если этого юзера то показываем, т.е. добавляем в общий контекст
        if self.object.usernew_id == self.request.user.id:
            context['lot'] = self.object
        else:
            raise Http404('Лот не найден')
        return context


def add_lot(request):
    o = Lot(lot_title=request.POST['title'], lot_text=request.POST['text'],
            lot_date=timezone.now(), usernew_id=request.user.id)
    print(request.user.pk)
    o.save(force_insert=True)
    return HttpResponseRedirect(reverse('lots:index'))
