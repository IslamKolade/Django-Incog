from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def home(request):
    return render(request, 'home.html')

def sw(request):
    return render(request, 'sw.js', content_type='application/javascript')

def fbsw(request):
    return render(request, 'firebase-messaging-sw.js', content_type='application/javascript')






