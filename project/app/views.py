from django.shortcuts import render

# Create your views here.



def hello(request):
    if request.method == 'GET':
        return render(request, 'test.html')

def Index(request):
    if request.method == 'GET':
        return render(request,'')