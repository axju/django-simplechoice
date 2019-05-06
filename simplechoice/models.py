from random import randint
from django.db import models
from django.utils.translation import ugettext_lazy as _


VALUE_KINDS = (
    ('min', 'Min'),
    ('max', 'Max'),
)


class Attribute(models.Model):
    name = models.CharField(_('attribute'), max_length=64)
    description = models.TextField(_('description'), default='...')
    start_min = models.IntegerField(default=80)
    start_max = models.IntegerField(default=100)

    def __str__(self):
        return self.name


class Decision(models.Model):
    question = models.TextField(_('question'))
    level = models.IntegerField(default=0)

    def __str__(self):
        return self.question[:30]

    class Meta:
        ordering = ('level', '?')

class DecisionRequireAttribute(models.Model):
    decision = models.ForeignKey(Decision, on_delete=models.CASCADE, related_name='requires')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='+')
    kind = models.CharField(_('value kind'), max_length=3, choices=VALUE_KINDS)
    value = models.IntegerField(default=1)

    def __str__(self):
        return '{} [{}]'.format(self.attribute.name, self.value)

class Answer(models.Model):
    decision = models.ForeignKey(Decision, on_delete=models.CASCADE, related_name='answers')
    name = models.CharField(_('name'), max_length=128)

    def __str__(self):
        return self.name[:30]

class AnswerGetAttribute(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='attributes')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='+')
    value = models.IntegerField(default=1)

    def __str__(self):
        return '{} [{}]'.format(self.attribute.name, self.value)


class Event(models.Model):
    EXIT_KINDS = (
        ('text', 'text'),
        ('exit', 'exit'),
    )
    name = models.CharField(_('name'), max_length=128)
    description = models.TextField(_('description'), default='')
    score = models.IntegerField(default=10)
    level_min = models.IntegerField(default=1)
    level_max = models.IntegerField(default=100)
    kind = models.CharField(_('kind'), default='text', max_length=8, choices=EXIT_KINDS)
    percent = models.FloatField(default=10)

    class Meta:
        ordering = ('?', )

    def __str__(self):
        return self.name

    def attributes_count(self):
        return self.attributes.count()
    attributes_count.short_description = 'attributes'


class EventAttribute(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attributes')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='events')
    kind = models.CharField(_('value kind'), max_length=3, choices=VALUE_KINDS)
    value = models.IntegerField(default=1)

    def __str__(self):
        return '{} [{} {}]'.format(self.attribute.name, self.kind, self.value)


class Game(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    key = models.CharField(_('key'), max_length=64)
    name = models.CharField(_('name'), max_length=256, null=True, blank=True)
    level = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    ranking = models.IntegerField(default=0)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return '{} - {}'.format(self.key, self.name)

    def decisions_count(self):
        return self.decisions.count()
    decisions_count.short_description = 'Decisions'

    def events_count(self):
        return self.events.count()
    events_count.short_description = 'Events'

    def score_percent(self):
        total = Game.objects.aggregate(models.Max('score'))
        return round(100 * ( self.score / total['score__max'] ))
    score_percent.short_description = 'Score %'

    def decisions_percent(self):
        count = self.decisions.filter(answer__isnull=False).count()
        open = self.decisions.filter(answer__isnull=True).count()
        total = self.get_decision_query().count()

        print(count, total)
        if open:
            return round(100 * ( count / (total + count + 1) ))
        elif total:
            return 0
        return 100
    decisions_percent.short_description = 'Decisions %'

    def events_percent(self):
        total = Event.objects.filter(kind='text', score__gt=0).count()
        return round(100 * ( self.events.count() / total ))
    events_percent.short_description = 'Events %'

    def update_ranking(self):
        i = 1
        for game in Game.objects.order_by('-score', '-level'):
            game.ranking = i
            game.save()
            i += 1

    def get_event_query(self):
        q = Event.objects.filter(level_min__lte=self.level, level_max__gte=self.level).exclude(games__game=self)
        for attribute in self.attributes.all():
            q = q.exclude(attributes__kind='min', attributes__attribute=attribute.attribute, attributes__value__gt=attribute.value)
            q = q.exclude(attributes__kind='max', attributes__attribute=attribute.attribute, attributes__value__lt=attribute.value)
        return q

    def get_event(self):
        print('check events')
        for event in self.get_event_query():
            n = randint(1,100)
            print(' ', event, n, event.percent)
            if n <= event.percent:
                return event
        return None

    def get_decision_query(self):
        q = Decision.objects.exclude(games__game=self)

        for attribute in self.attributes.all():
            q = q.exclude(requires__kind='min', requires__attribute=attribute.attribute, requires__value__gt=attribute.value)
            q = q.exclude(requires__kind='max', requires__attribute=attribute.attribute, requires__value__lt=attribute.value)

        return q

    @property
    def decision(self):
        """get the curent decision"""
        if self.event:
            return None

        game_decision = self.decisions.filter(answer__isnull=True).first()
        if game_decision:
            print('Have open decisions')
            return game_decision.decision

        decision = self.get_decision_query().first()
        if decision:
            print('Created new decisions')
            self.decisions.create(decision=decision)
            self.level = decision.level
            self.save()
            return decision

        self.update_ranking()
        return None

    @property
    def event(self):
        event = self.events.filter(seen=False).first()
        if event:
            return event.event
        return None

    def choice(self, choice):
        game_decision = self.decisions.filter(answer__isnull=True).first()
        if not game_decision:
            print('Error')
            return

        answer = Answer.objects.get(pk=choice)
        game_decision.answer = answer
        game_decision.save()
        print('Save answer {}'.format(answer))

        for attr in answer.attributes.all():
            attribute = self.attributes.get(attribute=attr.attribute)
            value = min(attribute.value + attr.value, attribute.value_max)
            attribute.value = max(value, 0)
            attribute.save()

        event = self.get_event()
        if event:
            self.events.create(event=event)

            if event.kind != 'exit':
                self.score += event.score
            else:
                self.update_ranking()
        self.save()

class GameDecision(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='decisions')
    decision = models.ForeignKey(Decision, on_delete=models.CASCADE, related_name='games')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+', null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.decision, self.answer)

class GameEvent(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='events')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='games')
    seen = models.BooleanField(default=False)

    def __str__(self):
        return '{} - {}'.format(self.event.name, self.event.kind)

class GameAttribute(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='attributes')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='games')
    value = models.IntegerField(default=1)
    value_max = models.IntegerField(default=100)

    def __str__(self):
        return self.attribute.name + ' -> ' + str(self.value) +'/' + str(self.value_max)
