from django.urls import path,re_path
from .views import HomeView,Image_to_Text_View,Text_to_speech_View,Image_to_Text_process_View
urlpatterns = [
    re_path(r'^$',HomeView,name='home'),
    re_path(r'^image_to_text/$',Image_to_Text_View,name="image-to-text"),
    re_path(r'^text_to_speech/$',Image_to_Text_View,name="text-to-speech"),
    re_path(r'^image_to_text_process/$',Image_to_Text_process_View,name = 'image_to_text_process'),
]