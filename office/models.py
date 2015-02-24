import yaml
import trafaret as t
from django.apps import apps
from django.conf import settings
from django.db import models
from django.db.models.fields import CharField, IntegerField, DateField


FIELDS_MAPPING = {
    'char': CharField,
    'int': IntegerField,
    'date': DateField
}

FIELDS_DEFAULT_KWARGS = {
    'char': {'max_length': 256}
}


class DynamicModel(models.Model):

    trafaret = t.Dict({
        t.Key('title', optional=True): t.String(allow_blank=True),
        t.Key('fields'): t.List(
            t.Dict({
                t.Key('id'): t.String(),
                t.Key('type'): t.Enum('char', 'int', 'date'),
                t.Key('title', optional=True): t.String(allow_blank=True)
            })
        )
    })

    class Meta:
        abstract = True

    @classmethod
    def all_models(cls, app_label=__package__):
        """Return all registered models for given app.
        By default returns models of current module."""

        models = apps.all_models

        if app_label:
            models = apps.all_models.get(app_label, {})

        return models

    @classmethod
    def get_model(cls, model_name, app_label=__package__):
        """Get model by name from registered models."""

        return apps.get_model(app_label, model_name)

    @classmethod
    def validate_loaded_models(cls, data):
        """Validate incoming data.

        :params dict data: Data dict
        :raises: DataError if data invalid
        """

        if not isinstance(data, dict):
            raise t.DataError('Expected dict in data file.')

        for name, params in data.items():
            cls.trafaret.check(params)

    @classmethod
    def load_models(cls, yaml_file):
        """Load data from yaml file and create models in memory.

        :param str yaml_file: Path to YAML file for load
        :raises: DataError if data in file invalid,
        YAMLError if file parse error
        """
        result = {}

        with open(yaml_file) as f:
            try:
                data = yaml.load(f.read())
            except yaml.YAMLError, exc:
                print "Error in configuration file:"
                raise exc

            cls.validate_loaded_models(data)

            for model_name, params in data.items():
                class Meta:
                    verbose_name = params.get('title', model_name)
                    verbose_name_plural = params.get('title', model_name)

                def __unicode__(self):
                    return u'{}: id {}'.format(
                        self._meta.verbose_name, str(self.id)
                    )

                model_params = {
                    '__module__': __name__,
                    '__unicode__': __unicode__,
                    'Meta': Meta
                }

                for field in params['fields']:
                    # add default kwargs to CharField
                    field_params = FIELDS_DEFAULT_KWARGS.get(field['type'], {})

                    model_params[field['id']] = FIELDS_MAPPING[field['type']](
                        field.get('title', field['id']), **field_params)

                result[model_name] = type(
                    model_name.capitalize(),
                    (models.Model, ),
                    model_params
                )

        return result


DynamicModel.load_models(settings.MODELS_PATH)
