from django.shortcuts import render

# Create your views here.
def mr_base(request):
    return render(request, 'mr_base.html')