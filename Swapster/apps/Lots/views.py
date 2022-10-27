from django.http import Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, FormView, UpdateView, DeleteView, CreateView

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
        # список лотов которые в свапах, возможно удалить список, т.к. никако информации в них не будет
        context['lots_in_swap_list'] = self.model.objects.filter(usernew_id=self.request.user.id, in_swap=True)\
            .order_by('-lot_date')
        # список моих свапов
        context['my_swaps_list'] = Swap.objects.filter(Q(lot_1__usernew_id=self.request.user.id) |
                                                             Q(lot_2__usernew_id=self.request.user.id))
        print(context['lots_in_swap_list'][0].id)
        print(context['my_swaps_list'][0].lot_1_id)
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
        context['title'] = self.object.lot_title
        # проверяем чей лот, если этого юзера то показываем, т.е. добавляем в общий контекст
        if self.object.usernew_id == self.request.user.id:
            context['lot'] = self.object
        else:
            raise Http404('Лот не найден')
        return context


class LotAdd(CreateView):
    model = Lot
    fields = ['lot_title', 'lot_text']
    template_name = 'lots/add.html'

    # def get_slug_field(self):

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добаваление'
        return context
    
    def form_valid(self, form):
        form.instance.lot_date = timezone.now()
        form.instance.usernew_id = self.request.user.id
        return super(LotAdd, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('lots:index')


class LotChange(UpdateView):
    model = Lot
    fields = ['lot_title', 'lot_text']
    template_name = 'lots/change.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование'
        return context

    def get_success_url(self):
        id = self.kwargs['pk']
        return reverse_lazy('lots:detail', kwargs={'lot_id': id})


class LotDelete(DeleteView):
    model = Lot
    template_name = 'lots/delete.html'

    def get_success_url(self):
        return reverse_lazy('lots:index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление'
        # проверяем чей лот, если этого юзера то показываем, т.е. добавляем в общий контекст
        if self.object.usernew_id == self.request.user.id:
            context['lot'] = self.object
        else:
            raise Http404('Лот не найден')
        return context
