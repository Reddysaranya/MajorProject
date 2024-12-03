from django.contrib import admin
from django.urls import path
from . import views
from django.urls import include, path

urlpatterns = [
    path('', views.home),
    path('about',views.about),
    path('home', views.home),
    path('features', views.features),
    path('usermain',views.usermain,name='usermain'),
    path('items_home',views.items_home,name='items_home'),
    path('child_bmi', views.child_bmi),
    path('blog',views.blog),
    path('post1',views.post1),
    path('post2',views.post2),
    path('post3',views.post3),
    path('post4',views.post4),
    path('post5',views.post5),
    path('post6',views.post6),
    path('yoga1',views.yoga1),
    path('yoga2',views.yoga2),
    path('yoga3',views.yoga3),
    path('yoga4',views.yoga4),
    path('bmi', views.bmi),
    path('bmi_predicted',views.bmi_predicted ,name="bmi_predicted"),
]