from django.shortcuts import render

# informational tools views
def index(request):
    return render(request, 'information/base.html')

def mtgrss(request):
    return render(request, 'information/mtgrss.html')

def youtube(request):
    return render(request, 'information/youtube.html')
