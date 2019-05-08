from django.contrib import admin
from nested_inline.admin import NestedTabularInline, NestedModelAdmin

from simplechoice.models import Attribute
from simplechoice.models import Game, GameDecision, GameAttribute, GameEvent
from simplechoice.models import Decision, DecisionRequireAttribute, Answer, AnswerGetAttribute
from simplechoice.models import Event, EventAttribute


class AttributeAdmin(admin.ModelAdmin):
    pass


class GameDecisionInline(admin.TabularInline):
    model = GameDecision


class GameAttributeInline(admin.TabularInline):
    model = GameAttribute


class GameEventInline(admin.TabularInline):
    model = GameEvent


class GameAdmin(admin.ModelAdmin):
    list_display = (
        'created_at', 'name', 'ranking', 'level', 'score', 'score_percent',
        'decisions_count', 'decisions_percent', 'events_count',
        'events_percent'
    )
    inlines = [GameDecisionInline, GameAttributeInline, GameEventInline]


class AnswerGetAttributeInline(NestedTabularInline):
    model = AnswerGetAttribute
    extra = 1
    fk_name = 'answer'


class AnswerInline(NestedTabularInline):
    model = Answer
    extra = 1
    fk_name = 'decision'
    inlines = [AnswerGetAttributeInline, ]


class DecisionRequireAttributeInline(NestedTabularInline):
    model = DecisionRequireAttribute
    extra = 1
    fk_name = 'decision'


class DecisionAdmin(NestedModelAdmin):
    model = Decision
    inlines = [DecisionRequireAttributeInline, AnswerInline]
    list_display = ('__str__', 'level')


class EventAttributeInline(admin.TabularInline):
    model = EventAttribute


class EventAdmin(admin.ModelAdmin):
    inlines = [EventAttributeInline, ]
    list_display = ('name', 'level_min', 'level_max', 'kind', 'percent', 'attributes_count')


admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Decision, DecisionAdmin)
admin.site.register(Event, EventAdmin)
