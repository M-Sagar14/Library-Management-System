from django.shortcuts import render,redirect
from django.http import HttpResponse
from UserApp.models import User
from django.contrib.auth.hashers import check_password,make_password
from AdminApp.models import Admin
import random,string
from django.core.mail import send_mail
from django.contrib import messages
from. import settings

def home(request):
    return render(request,'home.html')
def login(request):
    if request.method == 'POST':
        username_or_email = request.POST['username_or_email']
        password = request.POST['password']

        # if User.objects.get(Email = username_or_email,Password = password ):
        #     return HttpResponse("Successfully logged in")
        # else:
        #     return HttpResponse("Invalid details ")
        admin_user = Admin.objects.filter(Admin_Name=username_or_email).first() or Admin.objects.filter(Email=username_or_email).first()

        if admin_user:
            if check_password(password, admin_user.Password):
                request.session['admin_id'] = admin_user.Sno
                return redirect('AdminApp:dashboard')
            else:
                return HttpResponse("Invalid Admin Credentials")
        try:
            user=User.objects.get(Email = username_or_email)
            if user.Password == password:
                request.session['user_id'] = user.Sno
                return redirect('UserApp:dashboard')
        except User.DoesNotExist:
            try:
                 user=User.objects.get(Name = username_or_email )
                 if user.Password == password:
                    request.session['user_id'] = user.Sno
                    return redirect('UserApp:dashboard')
            except User.DoesNotExist:
                return HttpResponse("invalid details")

        
    return render(request,'login.html')
def forgot(request):
    if request.method == "POST":
        email = request.POST["email"]

        try:
            user = User.objects.get(Email = email)
            new = ''.join(random.choices(string.ascii_letters+string.digits,k=8))
            user.Password = new
            user.save()

            send_mail(
                "The New Password",
                f"Hello , {user.Name} \n Your New Password is : {new} \n After logging in please change your password \n Thank you",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False
            )

            messages.success(request, "A new password has been sent to your email.")
            return redirect("login")

        except User.DoesNotExist:
            return HttpResponse("No user found")
    return render(request,'forgot.html')

def create(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        
        if password == cpassword:
            user = User(Name=username,Email=email,Password=password)
            user.save()
            return redirect('login')
        else:
            return HttpResponse("Passwords doesn't matched")


    return render(request,'create.html')

