from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import pyrebase

config = {

    'apiKey': "AIzaSyDZxw1qSdXuHDLseNh2y3TN-O8NfhpPoQc",
    'authDomain': "cpanel-c54b7.firebaseapp.com",
    'databaseURL': "https://cpanel-c54b7.firebaseio.com",
    'projectId': "cpanel-c54b7",
    'storageBucket': "cpanel-c54b7.appspot.com",
    'messagingSenderId': "82198444165",
    'appId': "1:82198444165:web:eb9e20a95d9fcaacd991ec",
    'measurementId': "G-E595RHEXVP"
}

firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
database = firebase.database()


def signIn(request):
    try:
        request.COOKIES['uid']
    except:
        return render(request, "login.html")
    return redirect('/listdevices/')


def postsign(request):
    email = request.POST.get('email')
    passw = request.POST.get("pass")
    remembr_me = request.POST.get("remember-me")
    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        message = "invalid credentials"
        return render(request, "login.html", {"messg": message})
    print(user['idToken'])
    print(user['localId'])
    response = redirect("/dashboard")
    uid = user['localId']
    if not remembr_me:
        response.set_cookie('uid', uid)
    else:
        response.set_cookie('uid', uid, 2592000)
    return response


def logout(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie('uid')
    return response
