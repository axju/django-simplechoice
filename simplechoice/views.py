from django.shortcuts import redirect
from django.views import View
from django.views.generic import FormView, TemplateView
from django.views.generic import ListView
from django.urls import reverse_lazy

from django.utils.crypto import get_random_string
from simplechoice.models import Game, Attribute
from simplechoice.forms import NewGameForm, DecisionGameForm


class GameMixin(object):
    """docstring for GameMixin."""

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('game', ''):
            request.session['game'] = get_random_string(length=32)
        self.game, created = Game.objects.get_or_create(key=request.session['game'])
        if created:
            for attri in Attribute.objects.all():
                self.game.attributes.get_or_create(attribute=attri)
        return super(GameMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['game'] = self.game
        return super(GameMixin, self).get_context_data(**kwargs)


class GameIndex(GameMixin, FormView):
    template_name = 'simplechoice/index.html'
    success_url = reverse_lazy('simplechoice:index')

    def get_form(self, form_class=None):
        if not self.game.name:
            return NewGameForm(self.game, **self.get_form_kwargs())
        elif self.game.decision:
            return DecisionGameForm(self.game, **self.get_form_kwargs())
        self.game.update_ranking()
        return None

    def form_valid(self, form):
        form.save()
        return super(GameIndex, self).form_valid(form)


class GameContinue(GameMixin, View):

    def get(self, request, *args, **kwargs):
        if self.game.event and self.game.event.kind != 'exit':
            self.game.events.update(seen=True)
            self.game.save()
        return redirect('simplechoice:index')


class GameNew(View):

    def get(self, request, *args, **kwargs):
        del request.session['game']
        return redirect('simplechoice:index')


class GameDelete(View):

    def get(self, request, *args, **kwargs):
        if request.session.get('game', ''):
            self.game, created = Game.objects.get_or_create(key=request.session['game'])
            self.game.delete()
        return redirect('simplechoice:index')


class GameList(ListView):
    template_name = 'simplechoice/list.html'
    paginate_by = 20
    queryset = Game.objects.filter(ranking__gt=0).order_by('ranking')

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('game', ''):
            return super(GameList, self).dispatch(request, *args, **kwargs)

        self.game, created = Game.objects.get_or_create(key=request.session['game'])
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg)
        if not page:
            self.kwargs[self.page_kwarg] = int((self.game.ranking - 1) / self.paginate_by) + 1
        return super(GameList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['game'] = self.game
        return super(GameList, self).get_context_data(**kwargs)


class GameDebug(GameMixin, TemplateView):
    template_name = "simplechoice/debug.html"

    def get_context_data(self, **kwargs):
        kwargs['events'] = self.game.get_event_query()
        return super(GameDebug, self).get_context_data(**kwargs)
