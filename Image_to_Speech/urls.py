from django.urls import path,re_path
from .views import HomeView
urlpatterns = [
    re_path(r'^$',HomeView,name='home'),
]