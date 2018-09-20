from django.shortcuts import render

# builder views
def index(request):
    return render(request, 'builder/base.html')

def create(request):
    return render(request, 'builder/base.html')
