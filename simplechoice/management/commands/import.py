import os
import json
from django.core.management.base import BaseCommand
from simplechoice.models import Attribute, Decision, Event

class Command(BaseCommand):
    help = 'Import game data'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete curent game data',
        )

    def import_attributes(self, attributes):
        for attribute in attributes:
            attri, created = Attribute.objects.get_or_create(**attribute)
            self.stdout.write(self.style.SUCCESS('Add attribute {}'.format(attri.pk)))

    def import_questions(self, questions):
        for question in questions:
            decision, created = Decision.objects.get_or_create(**question['decision'])
            if not created:
                continue

            self.stdout.write(self.style.SUCCESS('Add decision {}'.format(decision.pk)))

            for require in question.get('requires', []):
                attri, _ = Attribute.objects.get_or_create(name=require.get('attribute', 'ERROR'))
                decision.requires.create(attribute=attri, kind=require.get('kind', 'min'), value=require.get('value', 1))

            for answer in question.get('answers', []):
                a = decision.answers.create(name=answer['text'])
                for data in answer.get('attributes', []):
                    attri, _ = Attribute.objects.get_or_create(name=data.get('attribute', 'ERROR'))
                    a.attributes.create(attribute=attri, value=data.get('value', 1))

    def import_events(self, events):
        for data in events:
            event, created = Event.objects.get_or_create(**data['event'])
            self.stdout.write(self.style.SUCCESS('Add event {}'.format(event.pk)))

            for attribute in data.get('attributes', []):
                attri, _ = Attribute.objects.get_or_create(name=attribute.get('attribute', 'ERROR'))
                event.attributes.create(attribute=attri, kind=attribute.get('kind', 'min'), value=attribute.get('value', 1))

    def import_file(self, filename):
        try:
            with open(filename, encoding='utf8') as json_file:
                data = json.load(json_file)

            self.import_attributes(data.get('attributes', []))
            self.import_questions(data.get('questions', []))
            self.import_events(data.get('events', []))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Cannot load file "{}"\n{}'.format(filename, e)))


    def handle(self, *args, **options):
        if options['delete']:
            Decision.objects.all().delete()
            Attribute.objects.all().delete()
            Event.objects.all().delete()

        if os.path.isdir(options['filename']):
            for filename in os.listdir(options['filename']):
                self.import_file(os.path.join(options['filename'], filename))
        else:
            self.import_file(options['filename'])
