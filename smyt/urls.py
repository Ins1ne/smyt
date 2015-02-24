from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from office.views import MainView, RoomViewSet, UserViewSet

router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'users', UserViewSet)


urlpatterns = patterns(
    '',
    url(r'^$', MainView.as_view(), name='main'),
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
