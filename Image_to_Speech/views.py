from django.shortcuts import render

# Create your views here.
def HomeView(request):
    if request.method == "POST":
        pass
    else:
        return render(request,'home.html')
def Image_to_Text_View(request):
    return render(request,'image_to_text.html')
def Image_to_Text_process_View(request):
    return render(request, 'home.html')
def Text_to_speech_View(request):
    pass