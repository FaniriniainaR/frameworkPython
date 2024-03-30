# my_app/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from .models import *
from django.utils.translation import gettext_lazy as _

#widget personnalisé: form asset:

global CSSPath, JSPath
CSSPath = {
            'all': ['css/bootstrap3.min.css', 'css/main.css', 
                    'wireframe-theme.min.css']
        }
JSPath = ['js/picturefill.min.js', 'js/jquery.min.js', 'js/outofview.js', 'js/bootstrap.min.js']

class TextWidget(forms.TextInput):
    class Media:
        css = CSSPath
        js = JSPath
    attrs = {'class':'form-control'}

class TextAreaWidget(forms.Textarea):
    class Media:
        css = CSSPath
        js = JSPath
    attrs = {'class':'form-control'}

class EmailWidget(forms.EmailInput):
    class Media:
        css = CSSPath
        js = JSPath
    attrs = {'class':'form-control'}

class PasswordWidget(forms.PasswordInput):
    class Media:
        css = CSSPath
        js = JSPath
    attrs = {'class':'form-control'}

class NumberWidget(forms.NumberInput):
    class Media:
        css = CSSPath
        js = JSPath
    attrs = {'class':'form-control'}

class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Mot de passe"),
        strip=False,
        widget=PasswordWidget(attrs={'class':'form-control', "autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Confirmez le mot de passe"),
        widget=PasswordWidget(attrs={'class':'form-control', "autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'address', 'job', 'telephone', 'ville' , 'password1', 'password2']
        widgets = {
            'name': TextWidget(attrs={'class':'form-control'}),
            'email': EmailWidget(attrs={'class':'form-control'}),
            'address': TextWidget(attrs={'class':'form-control'}),
            'job': TextWidget(attrs={'class':'form-control'}),
            'telephone': TextWidget(attrs={'class':'form-control'}),
            'ville': TextWidget(attrs={'class':'form-control'}),
        }
        labels = {
            'name': 'nom',
            'email': 'email',
            'address': 'addresse',
            'job': 'profession',
            'telephone': 'telephone',
            'ville': 'ville'
        }

class LoginForm(forms.Form):
    email = forms.EmailField(label="email", widget=EmailWidget(attrs={'class':'form-control'}))
    password = forms.CharField(label="mot de passe", widget=PasswordWidget(attrs={'class':'form-control'}))

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'address', 'job', 'telephone', 'ville']
        widgets = {
            'name': TextWidget(attrs={'class':'form-control'}),
            'email': EmailWidget(attrs={'class':'form-control'}), 
            'address': TextWidget(attrs={'class':'form-control'}),
            'job': TextWidget(attrs={'class':'form-control'}),
            'telephone': TextWidget(attrs={'class':'form-control'}),
            'ville': TextWidget(attrs={'class':'form-control'})
        }
        labels = {
            'name': 'nom',
            'email': 'email', 
            'address': 'addresse',
            'job': 'profession',
            'telephone': 'telephone',
            'ville': 'ville'
        }


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'description', 'notice', 'price']
        widgets = {
            'name': TextWidget(attrs={'class':'form-control'}),
            'description': TextAreaWidget(attrs={'class':'form-control'}),
            'notice': TextAreaWidget(attrs={'class':'form-control'}),
            'price': NumberWidget(attrs={'class':'form-control'})
        }
        labels = {
            'name': 'nom',
            'description': 'description',
            'notice': 'posologie',
            'price': 'prix'
        }


class SymptomeForm(forms.ModelForm):
    class Meta:
        model = Symptome
        fields = ['name', 'description', 'dangerousity']
        widgets = {
            'name': TextWidget(attrs={'class':'form-control'}),
            'description': TextAreaWidget(attrs={'class':'form-control'}),
            'dangerousity': NumberWidget(attrs={'class':'form-control'})
        }
        labels = {
            'name': 'nom',
            'description': 'description',
            'dangerousity': 'niveau de dangerosité'
        }


def get_symptome():
    listSymptome = Symptome.objects.all()
    choices = []
    for symptome in listSymptome:
        choices.append((symptome,symptome.name))
    return choices

class CurePatientForm(forms.Form):
    listSymptomField = forms.MultipleChoiceField(label = "Quels sont vos symptômes", widget = forms.CheckboxSelectMultiple, choices=get_symptome())
    

    