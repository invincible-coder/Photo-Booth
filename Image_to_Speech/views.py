from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest,HttpResponseRedirect
import Photo_Booth.tesseract
from django.core.files.storage import FileSystemStorage


# Create your views here.
def HomeView(request):
    return render(request,'home.html')
def Image_to_Text_View(request):
    if request.method == 'POST':
                    files = request.FILES['file'] 
                    fs = FileSystemStorage()
                    fs.save(files.name,files)
                    text = Photo_Booth.tesseract.transcript(files)
                    print(text)
                    response = JsonResponse({'message':"File Recieved successfully for processing.",'success':True,'text':text}) 
                    response.status_code = 200
                    return response
    return render(request,'image_to_text.html')

def Image_to_Text_process_View(request):
    return render(request, 'image_to_text.html')

def Text_to_speech_View(request):
    pass