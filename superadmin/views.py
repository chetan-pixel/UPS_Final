from django.http import HttpResponse
from django.shortcuts import render
from .models import user


def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')
        uid = request.POST.get('uid')
        remembr_me = request.POST.get("remember-me")
        print(email)
        print(password)
        print(uid)

        auth = run_authentication(email=email, password=password, uid=uid)
        if auth:
            response = HttpResponse("<h1>Login Success</h1>")
            if not remembr_me:
                response.set_cookie('admin_uid', uid)
            else:
                response.set_cookie('admin_uid', uid, 2592000)
            return response
        else:
            return HttpResponse("<h1>Error Login:Wrong Credentials</h1>")
    else:
        try:
            request.COOKIES['admin_uid']
        except:
            return render(request, 'superadmin/login.html')
        return HttpResponse("<h1>already login</h1>")


def run_authentication(email, password, uid):
    result = False
    try:
        userr = user.objects.filter(email=email, password=password)
        print(userr.first().uid)
        if str(userr.first().uid) == str(uid):
            result = True
    except:
        print("Error Login:Wrong Credentials")
    return result


def list_user(request):
    pass


def list_devices(request):
    pass