from django.views.generic import TemplateView
# from django.core.urlresolvers import reverse
from rest_framework import viewsets

from office.models import DynamicModel
from office.serializers import RoomSerializer, UserSerializer


class MainView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['links_list'] = [
            ('/users', DynamicModel.get_model('user')._meta.verbose_name),
            ('/rooms', DynamicModel.get_model('room')._meta.verbose_name)
        ]

        return context


class RoomViewSet(viewsets.ModelViewSet):
    queryset = DynamicModel.get_model('room').objects.all()
    serializer_class = RoomSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = DynamicModel.get_model('user').objects.all()
    serializer_class = UserSerializer
