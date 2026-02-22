from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('watches/', views.watch_list, name='watch_list'),
    path('watches/<slug:slug>/', views.watch_detail, name='watch_detail'),
    path('watches/<slug:slug>/review/', views.add_review, name='add_review'),
    path('search/', views.search, name='search'),
]
