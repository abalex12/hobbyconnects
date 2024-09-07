# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@cgu-odisha.ac.in'):
            raise forms.ValidationError("Email must be from the domain @cgu-odisha.ac.in")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user



# forms.py
from django import forms
from .models import Confession

class ConfessionForm(forms.ModelForm):
    class Meta:
        model = Confession
        fields = ['text', 'is_anonymous']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }

from django import forms
from .models import CustomUser, CrushRequest,Message




class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']



class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['bio', 'preferences']