from django.urls import path
from .views import index, about, send_data


urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('data/', send_data, name='send_data'),
]

