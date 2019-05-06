from django import forms


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
            print('error')
            return

        OPTIONS = [ (a.pk, a.name) for a in decision.answers.order_by('?')]
        self.fields['decision'] = forms.ChoiceField(label=decision.question, widget=forms.RadioSelect(), choices=OPTIONS)

    def save(self):
        print('Save form')
        print('Data', self.cleaned_data['decision'])
        self.game.choice(self.cleaned_data['decision'])
