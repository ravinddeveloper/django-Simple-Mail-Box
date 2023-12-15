from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from mailapp.models import *
from django.views.generic import View
from django.core.paginator import Paginator



from django.conf import settings
from django.core.mail import send_mail,EmailMessage
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,'index.html')

@login_required(login_url='login')
def dashboard(request):
        try:
          
            outbox=mail_data.objects.filter(user=request.user).order_by('reply','date')       
            inbox_mail=request.user.email
            inbox=mail_data.objects.filter(r_email=inbox_mail).order_by('read','date','reply')
            inbox_user=User.objects.all()
            verify=user_verify.objects.get(user=request.user)
            data={
                'data':outbox,
                'data2':inbox,
                'data3':verify,
                'users':inbox_user
            }
            return render(request,'dashboard.html',data)
            
        except Exception as e:
            messages.info(request,e)
        return render(request,'dashboard.html')
   
@login_required(login_url='login')
def mail_details(request,id):
    try:
        data=mail_data.objects.get(u_id=id)
        data.read='True'
        data.save()
        user=data.user
        data1=User.objects.get(username=user)
        return render(request,'mail_details.html',{'data':data,'data1':data1})
    except Exception as e:
        messages.info(request,e)
        return redirect("dashboard")
    return render(request,'mail_details.html')

class reply(View):
   
    def get(self,request,id):
        try:
            data=mail_data.objects.get(u_id=id)
            user=data.user
            data1=User.objects.get(username=user)
            return render(request,'reply.html',{'data':data,'data1':data1})
        except Exception as e:
            messages.info(request,e)
            return redirect("mail_details")
        return redirect("mail_details")
    def post(self,request,id):
        try:
            if request.method=="POST":
                data=mail_data.objects.get(u_id=id)
                msg=request.POST.get("reply_text")
                data.reply='True'
                data.reply_msg=msg
                data.save()
                messages.info(request,"Msg replied Successful")
                return redirect("dashboard")
        except Exception as e:
            messages.info(request,e)
            return redirect("mail_details")
        return redirect("mail_details")
        
@login_required(login_url='login')
def outbox(request,id):
    try:
        data=mail_data.objects.get(u_id=id)
        return render(request,'mail_details_outbox.html',{'data':data})
    except Exception as e:
        messages.info(request,e)
        return redirect("dashboard")
class send_mail(View):
   
   def get(self,request):
     return render(request,'send_mail.html')
   
   def post(self,request):
        try:
            if request.method=="POST":
                user=User.objects.get(username=request.user)
                email=request.POST.get('email_id')
                subject=request.POST.get('subject')
                msg=request.POST.get('msg')
                if email != user.email:
                    try:
                        iemail=User.objects.get(email=email)
                        if iemail is not None:
                            mail=mail_data.objects.create(user=user,r_email=email,subject=subject,msg=msg)
                            mail.save()
                            messages.info(request,"Message sent successfully")
                            return redirect("dashboard")
                        else:
                            messages.info(request,"Email not available")
                            return redirect("send")
                    except Exception as e:
                        messages.info(request,"Email Not Found")
                        return redirect("send")
                else:
                    messages.info(request,"You can't send Mail to yourself")
                    return redirect("send")
            return redirect("send")
        except Exception as e:
            messages.warning(request,e)
            return redirect("send")
    




from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_str
@login_required(login_url='login')
def send_verify_link(request):
    try:
        user=User.objects.get(username=request.user)
        e_code=urlsafe_base64_encode(str(user).encode('utf-8'))
        link=f'http://127.0.0.1:8000/verify/{e_code}'
        subject = 'Verify Your email'
        message = f'Hi , please verify the using this link."{link}"'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        email_msg=EmailMessage(subject, message, email_from, recipient_list )
        email_msg.send()
        return redirect(dashboard)
    except Exception as e:
        messages.info(request,e)   
        return redirect("dashboard")

@login_required(login_url='login')
def verify_link(request,id):
    try:
        d_code=urlsafe_base64_decode(id)
        d_code=force_str(d_code)
        user=user_verify.objects.get(user=d_code)
        user.verify=True
        user.save()
        return render(request,'verified.html')
    except Exception as e:
        messages.info(request,e)   
        return redirect("login")