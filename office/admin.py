from django.contrib import admin

from office.models import DynamicModel


# Dynamically register models for admin
for name, instance in DynamicModel.all_models().items():
    admin.site.register(instance)
