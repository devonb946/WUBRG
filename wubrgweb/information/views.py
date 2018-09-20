from django.shortcuts import render

# informational tools views
def index(request):
    return render(request, 'information/base.html')

def youtube(request):
    return render(request, 'information/base.html')

def articles(request):
    return render(request, 'information/base.html')

def tutorials(request):
    return render(request, 'information/base.html')
