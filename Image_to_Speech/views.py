from django.shortcuts import render

# Create your views here.
def HomeView(request):
    if request.method == "POST":
        pass
    else:
        return render(request,'home.html')