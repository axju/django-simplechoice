from django import forms
from django.http import Http404

class BasicGameForm(forms.Form):

    def __init__(self, game, *args, **kwargs):
        super(BasicGameForm, self).__init__(*args, **kwargs)
        self.game = game


class NewGameForm(BasicGameForm):
    name = forms.CharField()

    def save(self):
        self.game.name = self.cleaned_data['name']
        self.game.save()


class DecisionGameForm(BasicGameForm):

    def __init__(self, game, *args, **kwargs):
        super(DecisionGameForm, self).__init__(game, *args, **kwargs)

        decision = self.game.decision
        if not decision:
            raise Http404("No more questions")

        OPTIONS = [ (a.pk, a.name) for a in decision.answers.order_by('?')]
        self.fields['decision'] = forms.ChoiceField(
            label=decision.question,
            widget=forms.RadioSelect(),
            choices=OPTIONS
        )

    def save(self):
        self.game.choice(self.cleaned_data['decision'])
