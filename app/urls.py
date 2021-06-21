from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views




urlpatterns = [
        path('', views.login, name='login'),
        path('logout', views.logout, name='logout'),
        path('home', views.home, name='home'),
        path('split_data', views.split_data, name='split_data'),
        path('get_audio_clips', views.get_audio_clips, name='get_audio_clips'),
        path('evaluate', views.evaluate, name='evaluate'),
        path('next', views.next, name='next'),


              ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_name = 'app'
