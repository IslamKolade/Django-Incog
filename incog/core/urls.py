from django.urls import path
from . import views
from django.conf.urls import include
from fcm_django.api.rest_framework import FCMDeviceViewSet, FCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

router = DefaultRouter()
router.register('devices', FCMDeviceAuthorizedViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('sw.js', views.sw, name='sw'),
    path('docs/', include_docs_urls(title='FCM django web demo')),
    path('routes/', include(router.urls)),
    path('firebase-messaging-sw.js', views.fbsw, name='fbsw'),
]
