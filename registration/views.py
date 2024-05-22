from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib import messages

UserModel = get_user_model()




def user_signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        try:
            if request.method == 'POST':
                username = request.POST['username']
                email = request.POST['email']
                pass1 = request.POST['password1']
                pass2 = request.POST['password2']

                pre_username = User.objects.filter(username=username)
                pre_email = User.objects.filter(email=email)

                if pass1 == pass2:
                    user = User.objects.create(
                        username=username,             
                        email=email,
                    )
                    user.set_password(pass1)
                    user.is_active = False
                    user.save()

                    current_site = get_current_site(request)
                    message_sub = "Verify your email"
                    message = render_to_string("registration/activate.html", {
                        "user":user,
                        "domain":current_site.domain,
                        "uid":urlsafe_base64_encode(force_bytes(user.pk)),
                        "token":default_token_generator.make_token(user)
                    })
                    send_email = email
                    email = EmailMessage(message_sub,message,to=[send_email])
                    email.send()
                    messages.success(request, "Account created successfully !")
                    return render(request, "registration/message.html")
                elif pre_email or pre_username:
                    user = User.objects.create(
                        username=username,             
                        email=email,
                    )
                    user.set_password(pass1)
                    user.is_active = False
                    user.save()

                    current_site = get_current_site(request)
                    message_sub = "Verify your email"
                    message = render_to_string("registration/activate.html", {
                        "user":user,
                        "domain":current_site.domain,
                        "uid":urlsafe_base64_encode(force_bytes(user.pk)),
                        "token":default_token_generator.make_token(user)
                    })
                    send_email = email
                    email = EmailMessage(message_sub,message,to=[send_email])
                    email.send()
                    messages.success(request, "Account created successfully !")
                    return render(request, "registration/message.html")
                else:
                    messages.error(request, "Something went wrong !")
                    return redirect('signup') 
        except Exception as e:
            print(e)
            messages.error(request, e)
            return redirect('signup')
  
        return render(request, 'registration/signup.html')



def activate(request, uid, token):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        try:
            u_id = urlsafe_base64_decode(uid).decode()
            user = UserModel._default_manager.get(pk=u_id)
        except Exception as e :
            user = None
            return HttpResponse(e)
        if user is not None and default_token_generator.check_token(user,token):
            user.is_active = True
            user.save()
            messages.success(request, "Account verified successfully. Now login your account !")
            return redirect("login")
        else:
            messages.error(request, "Account not verified !")
            return redirect("signup")
            





def user_login(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        try:
            if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request,username=username,password=password)

                if user is not None:
                    login(request, user)
                    messages.success(request, "Logged in successfully !")
                    return redirect('home')
                else:
                    messages.error(request, "Enter valid info and try again !")
                    return redirect('login')
        except Exception as e:
               messages.error(request, e)
               return redirect('login')     
        
        return render(request, 'registration/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully !")
    return redirect('login')



