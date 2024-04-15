from django.shortcuts import render

# Create your views here.
def fgrn_base(request):
    return render(request, 'fgrn_base.html')