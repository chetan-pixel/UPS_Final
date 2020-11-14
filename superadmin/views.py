from django.http import HttpResponse
from django.shortcuts import render
from .models import user


def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')
        uid = request.POST.get('uid')
        print(email)
        print(password)
        print(uid)
        auth = run_authenticattion(email=email,password=password,uid=uid)
        return HttpResponse("<h1>Done</h1>")
    else:
        return render(request, 'superadmin/login.html')



# def list_users(request):


def run_authenticattion(email, password, uid):
    result = False
    try:
        userr = user.objects.filter(email=email,password=password)
        print(userr.first().uid)
        if userr.first().uid == uid:
           result = True
    except:
        print("Error Login:Wrong Credentials")
    return True