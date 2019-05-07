from django.test import TestCase
from django.core.management import call_command

from simplechoice.models import Game

class GameTestCase(TestCase):

    def setUp(self):
        call_command('import', 'tests/data.json')

    def test_game_defaults(self):
        game = Game.objects.create(name="user")
        self.assertEqual(game.score, 0)
        self.assertEqual(game.ranking, 0)
        self.assertEqual(game.level, 0)

    def test_game_play(self):
        game = Game.objects.create(name="user")
        self.assertEqual(game.score, 0)

        while game.decision:
            answer = game.decision.answers.filter(name="attri1").first()
            game.choice(answer.pk)

            if game.event:
                print(game.event.name)

        #self.assertEqual(game.event.name, "event1")
        #self.assertEqual(game.event.name, "event1")
        #self.assertEqual(game.score, 50)
