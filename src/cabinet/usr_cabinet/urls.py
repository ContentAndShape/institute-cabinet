from django.urls import path

from . import views


app_name = 'usr_cabinet'
urlpatterns = [
    path('', views.cabinet, name='render_cabinet'),
]
