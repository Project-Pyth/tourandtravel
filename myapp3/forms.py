from django import forms
from django.contrib.auth.models import User
from myapp3.models import userprofile

class userupdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username']

class profileupdate(forms.ModelForm):
    class Meta:
        model = userprofile
        fields = ['email','contact','city','image']
