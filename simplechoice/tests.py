from io import StringIO

from django.test import TestCase
from django.core.management import call_command

from simplechoice.models import Game


class GameTestCase(TestCase):

    def test_game_defaults(self):
        game = Game.objects.create(name="user")
        self.assertEqual(game.score, 0)
        self.assertEqual(game.ranking, 0)
        self.assertEqual(game.level, 0)

    def test_import(self):
        out = StringIO()
        call_command('import', 'tests/data.json', stdout=out)
        self.assertIn('Add attribute', out.getvalue())
        self.assertIn('Add event', out.getvalue())
        self.assertIn('Add decision', out.getvalue())
