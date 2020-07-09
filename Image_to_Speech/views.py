from django.shortcuts import render
from .forms import ImageUploadForm
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
# Create your views here.
def HomeView(request):
    return render(request,'home.html')
def Image_to_Text_View(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST,request.FILES)
        if form.is_valid():
            if form.validate_size():
                if form.validate_file_type():
                    file = form.cleaned_data['file']
                    #call the process function here.
                    response = JsonResponse({'message':"File Recieved successfully for processing.",'success':True})
                else:
                    response = JsonResponse({'message':"Invalid file type.",'success':False})
                    print('1')    
            else:
                response = JsonResponse({'message':"File size limit exceeds.",'success':False})
                print('2')
        else:
            response = JsonResponse({'message':"You need to upload a file.",'success':False})
            print('3')
        response.status_code = 200
        return response
    return render(request,'image_to_text.html')
def Image_to_Text_process_View(request):
    return render(request, 'home.html')
def Text_to_speech_View(request):
    pass