from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.receive_url, name='shorten'),
    path('<str:short_code>/', views.redirect_to_long, name='redirect'),
]
