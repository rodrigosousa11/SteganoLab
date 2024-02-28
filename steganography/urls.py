from django.urls import path

from capstone import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('encode', views.encode_image, name='encode'),
    path('decode', views.decode_image, name='decode'),
    path('history', views.history_view, name='history')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)