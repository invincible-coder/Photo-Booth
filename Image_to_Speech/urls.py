from django.urls import path,re_path
from .views import HomeView,Image_to_Text_View,Text_to_speech_View,clearFilesView,downloadFile
urlpatterns = [
    re_path(r'^$',HomeView,name='home'),
    re_path(r'^image_to_text/$',Image_to_Text_View,name="image_to_text"),
    re_path(r'^text_to_speech/$',Image_to_Text_View,name="text_to_speech"),
    re_path(r'^clearFiles/$',clearFilesView,name = 'clearFiles'),
    path('Photo_Booth/static/results/<str:filename>',downloadFile,name = 'downloadFile')
]