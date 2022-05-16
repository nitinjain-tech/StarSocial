from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView,TemplateView
from django.contrib import messages
from .models import Profile
import uuid

from django.conf import settings
from django.core.mail import send_mail




from . import forms
# Create your views here.



class SignUp(CreateView):

    form_class = forms.UserCreateForm
    success_url = reverse_lazy('accounts:token_send')
    template_name = 'accounts/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        # email = request.POST.get('email')
        if form.is_valid():

            new_user = form.save()
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password1')
            # user.is_verified = False # Deactivate account till it is confirmed
            # new_user.save()

            token = uuid.uuid4()
            print(token)
            auth_token = str(uuid.uuid4())
            pro_obj = Profile.objects.create(user = new_user,auth_token = auth_token)
            pro_obj.save()
            send_mail_after_registration(email,auth_token)

            return render(request ,'accounts/token_send.html')
        else:
            print(form.errors)
            return render(request ,'accounts/error.html')


    # def __init__(self):
    #     token = uuid.uuid4()
    #     # print(token)

    # def register_attempt(self,request):

        # print(str(uuid.uudi4()))

        # if request.method == 'POST':
        #     username = request.POST.get('username')
        #     email = request.POST.get('email')
        #     password = request.POST.get('password1')
        #
        #     try:
        #
        #         user_obj = User(username = username , email = email)
        #         user_obj.set_password(password)
        #         user_obj.save()

        #         auth_token = str(uuid.uuid4())

        #         profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
        #         profile_obj.save()

        #         print(auth_token)
        #         send_mail_after_registration(email,auth_token)
        #         return redirect('accounts/token')
        #
        #     except Exception as e:
        #         print(e)
        #
        # return render(request , 'accounts/signup.html')



class Success(TemplateView):
    template_name = 'accounts/success.html'

class Token_send(TemplateView):
    template_name = 'accounts/token_send.html'
    # success_url = reverse_lazy('token_send')

# class Verify(TemplateView):
def verify(request,auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
                # if profile_obj.is_verified:
                #     messages.success(request,"Your account is already verified")
                #     return redirect('accounts/login')

            profile_obj.is_verified= True
            profile_obj.save()
            messages.success(request,"Your account has been verified")
            return render(request,'accounts/success.html')
        else:
            return render(request,'accounts/error.html')
    except Exception as e:
        print(e)


class Error(TemplateView):
    template_name = 'accounts/error.html'
    def error_page(request):
        return render(request,'accounts/error.html')



# class SendMail(TemplateView):

def send_mail_after_registration(email,auth_token):
    subject = "Verify your Star-Social account!"
    message = f'Hi! Click the link to verify your account:  http://127.0.0.1:8000/accounts/verify/{auth_token}'
    email_from = settings.EMAIL_HOST_USER
    receipient_list = [email]
    send_mail(subject,message,email_from,receipient_list)
