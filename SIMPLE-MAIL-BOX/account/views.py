from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from mailapp.models import *
from django.views.generic import View
from django.contrib.auth.decorators import login_required


# Create your views here.
def handle_login(request):
    try:
        if request.method=="POST":
            uname=request.POST.get('uname')
            pass1=request.POST.get('pass1')
            user=authenticate(request,username=uname,password=pass1)
            if user is not None:
                messages.info(request,"Login Success")
                login(request,user)
                return redirect('dashboard')
    except Exception as e:
        messages.info(request,e)
        return render(request,'login.html')
    return render(request,'login.html')

def register(request):
    try:
        if request.method=="POST":
                first_name=request.POST.get("fname")
                last_name=request.POST.get("lname")
                mail=request.POST.get("email")
                username=request.POST.get("uname")
                pass1=request.POST.get("pass1")
                pass2=request.POST.get("pass2")
                user=User.objects.filter(username=username)
                user1=User.objects.filter(email=mail)
                if user.exists():
                    messages.info(request,"username already taken")
                    return redirect("register")
                elif user1.exists():
                    messages.info(request,"user with this email is already exists")
                    redirect("register")

                elif pass1 !=pass2:
                    messages.info(request,"Password is not match")
                    return redirect("register")

                else: 
                           
                    user2=User.objects.create(first_name=first_name,last_name=last_name,email=mail,username=username)
                    user2.set_password(pass1)
                    user2.save()
                    v_user=user_verify.objects.create(user=username) 
                    v_user.save()   
                    messages.info(request,"Registered Successfully")
                    return render(request,'register.html')
    except Exception as e:
        messages.info(request,e)
    return render(request,'register.html')

@login_required(login_url='login')
def handle_logout(request):
    logout(request)
    messages.info(request,"logout successful")
    return render(request , "login.html")



class profile(View):
    
    def get(self,request):
        try:
            username=request.user
            data=user_verify.objects.get(user=username)
            return render(request,'profile.html',{'data':data})
        except Exception as e:
            messages.info(request,e)
        return render(request,'profile.html')
    def post(self,request):
        try:
            u_name=request.user
            pass1=request.POST.get('pass1')
            user=authenticate(request,username=u_name,password=pass1)
            if user is not None:
                return render(request,'reset_password.html')
            else:
                messages.info(request,"Enter Valid Password")
                return redirect('profile')
        except Exception as e:
            messages.info(request,e)
        return redirect('profile')

@login_required(login_url='login')
def reset_password(request):
    try:
        if request.method=="POST":
            user=request.user
            pass1=request.POST.get("pass1")
            pass2=request.POST.get("pass2")
            if pass1 != pass2:
                messages.info(request,"Password is not Matching!")
                return render(request,'reset_password.html')
            else:
                user=User.objects.get(username=user)
                user.set_password(pass1)
                user.save()
                login(request,user)
                messages.info(request,"Password Reset Successfully")
                return redirect('profile')
                
    except Exception as e:
        messages.info(request,e)
        return render(request,'reset_password.html')
