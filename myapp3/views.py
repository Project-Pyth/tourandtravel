from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth,User
from django.contrib.auth import login
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from myapp3.models import packages_tour, booking_detail
from myapp3.tokens import account_activation_token
from myapp3.forms import userupdate, profileupdate
from myapp3.models import userprofile
from .models import contact
from django.views.decorators.csrf import csrf_exempt
from myapp3.paytm import Checksum
MERCHANT_KEY = 'FPj0FruZZ!bVmkc0';


from paypal.standard.forms import PayPalPaymentsForm
from tourandtravel import settings
from django.urls import reverse


def index(request):
    return render(request,'index.html')

def nav(request):
    return render(request,'nav.html')

def Login(request):
    if request.method == 'POST':
        un = request.POST['uname']
        pass1=request.POST['pass']

        user=auth.authenticate(username=un,password=pass1)
        if user is not None:
            auth.login(request,user)
            return redirect('/index')
        else:
            messages.info(request,'invalid credentials')
            return redirect('Login')
    else:
         return render(request,'Login.html')

def logout(request):
    auth.logout(request)
    return redirect('/index')

def registration(request):
    if request.method == 'POST':
        fn=request.POST['fname']
        ln=request.POST['lname']
        un=request.POST['uname']
        em=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']


        if pass1 == pass2:

            if User.objects.filter(username=un).exists():
                messages.info(request,'Username Already Taken')
                return redirect('/registration')
            elif User.objects.filter(email=em).exists():
                messages.info(request,'Email Taken')
                return redirect('/registration')
            else:
                user=User.objects.create_user(username=un, email=em, password=pass1, first_name=fn, last_name=ln)
                user.is_active = False
                user.save()

                current_site = get_current_site(request)
                subject = 'Activate Your MySite Account'
                message = render_to_string('acc_active_email.html',
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                #send_mail(
                    #"Hello User",
                    #"Welcome to Email Confirmation",
                    #"btesinstitute74@gmail.com",
                    #[em],
                    #fail_silently=False,
                #)
                send_mail(
                    subject,
                    message,
                    'btesinstitute74@gmail.com',
                    [em],
                    fail_silently=False,
                )
                messages.info(request,'you are registered successfully !! Please Confirm your Email address')
                return redirect('/registration')
        else:
            print('password not matched !')
            messages.info(request,'registration')
            return redirect('/registration')
    else:
        return render(request,"registration.html")

def learnmore(request):
    return render(request,'learnmore.html')


def contactus(request):
    if request.method == "POST":
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')

        contacts = contact(name=name, email=email,phone=phone, desc=desc)
        contacts.save()
        messages.success(request,'Your Query Successfully Submitted.')
        return render(request,'contactus.html')
    else:
        return render(request,'contactus.html')

class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            #uid = force_text(urlsafe_base64_decode(uidb64))
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profilee.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            print("confirmed",user.is_active)
            return render(request,'index.html',{"data":user.first_name,"Flag":True})
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('/index')

def tourpackages(request):
    packages = packages_tour.objects.all()
    print(packages)
    context = {'packages':packages}
    return render(request,'tourpackages.html',context)

def viewdetail(request):
    context = {}
    id = request.GET["package_id"]
    obj = packages_tour.objects.get(id=id)
    context["packages_tour"] = obj
    return render(request,'viewdetail.html',context)

def booknow(request):
    if request.method == "POST":
        name=request.POST.get('name','')
        contact=request.POST.get('contact','')
        address=request.POST.get('address','')
        email=request.POST.get('email','')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        from_date=request.POST.get('from_date','')
        to_date=request.POST.get('to_date','')

        books = booking_detail(name=name,contact=contact,address=address, email=email, city=city, state=state, from_date=from_date, to_date=to_date)
        books.save()
        messages.success(request,'Your booking detail are Successfully Submitted.')
        return redirect('/process_payment')
    else:
        context = {}
        id = request.GET["package_id"]
        obj = packages_tour.objects.get(id=id)
        context["packages_tour"] = obj
        return render(request,'booknow.html',context)

def paymentMode(request):
        # request paytm to transfer the amount to your account after payment by user
        param_dict = {
            'MID':'YPysuN67523765743950',
            'ORDER_ID':'645',
            'TXN_AMOUNT':'1',
            'CUST_ID':'3',
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
	        'CALLBACK_URL':'http://merchant.com/callback/',
        }
        param_dict['CHACKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request,'paytm.html',{'param_dict':param_dict})


@csrf_exempt
def handlerequest(request):
    #paytm will send you post request here.
   return redirect('/index')



@login_required
def userprofile(request):
    if request.method == 'POST':
        u_form = userupdate(request.POST, instance=request.user)
        p_form = profileupdate(request.POST, request.FILES, instance=request.user.userprofile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
    else:
        u_form = userupdate(instance=request.user)
        p_form = profileupdate(instance=request.user.userprofile)
    return render(request,"userprofile.html",{'u_form':u_form,'p_form':p_form})

def viewprofile(request):
    return render(request,'viewprofile.html')

def developers(request):
    return render(request,'developers.html')

def process_payment(request):

    paypal_dict = {
        'business':settings.PAYPAL_RECEIVER_EMAIL,
        'amount':'',
        'item_name':"abcd",
        'invoice':"1",
        'notify_url':'http://{}{}'.format("127.0.0.1:8000",reverse('paypal-ipn')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request,'process_payment.html',{'form':form})
