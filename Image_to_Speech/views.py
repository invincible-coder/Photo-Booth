from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest,HttpResponseRedirect
import Photo_Booth.tesseract
from django.core.files.storage import FileSystemStorage
from .forms import ImageUploadForm
from fpdf import FPDF
from django.views.decorators.csrf import csrf_exempt
from Photo_Booth import settings
import mimetypes
# Create your views here.
def HomeView(request):
    return render(request,'home.html')
def Image_to_Text_View(request):
    if request.method == 'POST':
        print(request.FILES)
        form = ImageUploadForm(request.POST,request.FILES)
        if form.is_valid():
            if form.validate_size():
                if form.validate_file_type():
                    files = form.cleaned_data['files']
                    fs = FileSystemStorage()
                    fs.save(files.name,files)
                    try:
                        text = Photo_Booth.tesseract.transcript(files)
                    except Exception:
                        response = JsonResponse({'message':"File could not be read.","success":False})
                        response.status_code = 200
                        return response
                    #print(text)
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font('Helvetica',style='')
                    filename = files.name.split('.')[0]
                    path = "Photo_Booth/static/results/{}.pdf".format(filename)
                    print("path = ",path)
                    text.encode('utf-8').strip()
                    try:
                        pdf.multi_cell(0,5,text)
                        pdf.output(path,'F').encode("utf-8")
                        print("file outputed")
                    except UnicodeEncodeError:
                        response = JsonResponse({'message':"Text could not be converted to pdf",'success':True,'text':text})
                        response.status_code = 200
                        return response          
                    response = JsonResponse({'message':"File converted successfully",'success':True,'text':text,'path':path})
                else:
                    print('1')
                    response = JsonResponse({'message':"Invalid file type.",'success':False})
            else:
                print('2')
                response = JsonResponse({'message':"File size limit exceeds.",'success':False})
        else:
            response = JsonResponse({'message':"facing validation errors",'success':False})
            print('3')
        response.status_code = 200
        return response 
    return render(request,'image_to_text.html')
@csrf_exempt
def downloadFile(request,filename):
    path = 'Photo_Booth/static/results/' + filename
    with open(path,'rb') as f:
        response = HttpResponse(f)
        response['Content-Type'] = 'application/pdf'
        response['Content-disposition'] = 'attachment ; filename = {}'.format(filename)
        return response

@csrf_exempt
def clearFilesView(request):
    pass
def Text_to_speech_View(request):
    pass