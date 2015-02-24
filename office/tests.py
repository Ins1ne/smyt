import os
from datetime import datetime

import yaml
import trafaret as t
from django.core import management
from django.conf import settings
from django.db import models
from django.test import TestCase

from .models import DynamicModel


class DynamicModelTestCase(TestCase):

    def setUp(self):
        data = {
            'test': {
                'title': 'Test Model',
                'fields': [
                    {'id': 'name', 'type': 'char', 'title': 'Name Field'},
                    {'id': 'number', 'type': 'int', 'title': 'Number Field'},
                    {'id': 'date', 'type': 'date', 'title': 'Date Field'},
                ]
            }
        }
        self.yaml_file = '/tmp/models.yaml'

        with open(self.yaml_file, 'w+') as file:
            file.write(yaml.dump(data))

        self.migrations_path = os.path.join(
            settings.BASE_DIR, '..', 'office', 'migrations'
        )
        self.migrations = os.listdir(self.migrations_path)

    def tearDown(self):
        if os.path.exists(self.yaml_file) and os.path.isfile(self.yaml_file):
            os.unlink(self.yaml_file)

        # cleanup created migrations
        for file in os.listdir(self.migrations_path):
            if file not in self.migrations:
                os.unlink(os.path.join(self.migrations_path, file))

    def test_load_models(self):
        result = DynamicModel.load_models(self.yaml_file)

        self.assertIn('test', result)
        self.assertEqual(result['test']._meta.verbose_name, 'Test Model')
        self.assertEqual(len(result['test']._meta.fields), 4)

    def test_load_models_with_wrong_yaml_data(self):
        yaml_file = '/tmp/models_{}'.format(self.id())

        with open(yaml_file, 'w+') as file:
            file.write(yaml.dump('test'))

        with self.assertRaises(t.DataError):
            DynamicModel.load_models(yaml_file)

    def test_validate_loaded_models_without_optional_keys(self):
        data = {
            'test': {
                'fields': [
                    {'id': 'name', 'type': 'char'},
                    {'id': 'number', 'type': 'int'},
                    {'id': 'date', 'type': 'date'},
                ]
            }
        }
        yaml_file = '/tmp/models_{}'.format(self.id())

        with open(yaml_file, 'w+') as file:
            file.write(yaml.dump(data))

        result = DynamicModel.load_models(yaml_file)

        self.assertIn('test', result)
        self.assertEqual(result['test']._meta.verbose_name, 'test')
        self.assertEqual(len(result['test']._meta.fields), 4)

    def test_validate_loaded_models_without_some_keys(self):
        data = {
            'test': {
                'fields': [
                    {'id': 'name', 'type': 'charfield'},
                    {'id': 'number'},
                    {'id': 'date', 'type': 'date'},
                ]
            }
        }
        yaml_file = '/tmp/models_{}'.format(self.id())

        with open(yaml_file, 'w+') as file:
            file.write(yaml.dump(data))

        with self.assertRaises(t.DataError):
            DynamicModel.load_models(yaml_file)

    def test_all_models(self):
        DynamicModel.load_models(self.yaml_file)
        result = DynamicModel.all_models()

        self.assertIn('test', result)

    def test_get_models(self):
        DynamicModel.load_models(self.yaml_file)
        model = DynamicModel.get_model('test')

        self.assertTrue(issubclass(model, models.Model))
        self.assertEqual(len(model._meta.fields), 4)
        self.assertEqual(model.__name__, 'Test')

    def test_created_model(self):
        DynamicModel.load_models(self.yaml_file)
        management.call_command('makemigrations', 'office')
        management.call_command('migrate', 'office')
        model = DynamicModel.get_model('test')

        model.objects.create(
            name='test_name',
            number=1,
            date=datetime.strptime('2015-01-01', '%Y-%m-%d').date()
        )

        self.assertEqual(model.objects.count(), 1)

        instance = model.objects.get(pk=1)

        self.assertEqual(instance.name, 'test_name')
