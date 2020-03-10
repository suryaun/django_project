from django import forms
from django.contrib.auth.models import User
from basic_app.models import User_Profile

def email_validator(value):
    current_email = [i.email for i in User.objects.all()]
    if value in current_email:
        raise forms.ValidationError("This email already exists")

class Userform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(validators=[email_validator])
    class Meta():
        model = User
        fields = ('first_name','last_name','email','username','password')

class UserProfileForm(forms.ModelForm):
    class Meta():
        model = User_Profile
        fields = ('portfolio_site','profile_pic')
