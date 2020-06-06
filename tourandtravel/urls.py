"""tourandtravel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from myapp3 import views
from myapp3.views import ActivateAccount
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('activate/<uidb64>/<token>/',ActivateAccount.as_view(),name='activate'),
    url('index/',views.index,name='index'),
    url('nav/',views.nav,name='nav'),
    url('Login/',views.Login,name='Login'),
    url('logout/',views.logout,name='logout'),
    url('registration/',views.registration,name='registration'),
    url('learnmore/',views.learnmore,name='learnmore'),
    url('contactus/',views.contactus,name='contactus'),
    url('tourpackages/',views.tourpackages,name='tourpackages'),
    url('viewdetail/',views.viewdetail,name='viewdetail'),
    url('booknow/',views.booknow,name='booknow'),
    #url('handlerequest/',views.handlerequest,name='handle'),
    #url('paymentMode/',views.paymentMode,name='handle'),
    url('userprofile/',views.userprofile,name='userprofile'),
    url('viewprofile/',views.viewprofile,name='viewprofile'),
    url('developers/',views.developers,name='developers'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('process_payment/',views.process_payment,name='process_payment'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
