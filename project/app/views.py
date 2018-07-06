from django.shortcuts import render

# Create your views here.



def hello(request):
    if request.method == 'GET':
        return render(request, 'base.html')
