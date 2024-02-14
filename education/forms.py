from django import forms
from .models import CustomUser, Contact, Shartnoma

class CustomUserFormUpdateProfile(forms.ModelForm):
    # password = forms.CharField(max_length=120 ,widget=forms.PasswordInput)
    tavallud_sanasi = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    class Meta:
        model = CustomUser
        fields = ['username','first_name', 'last_name', 'email', 'IDNumber', 'telefon', 'tavallud_sanasi', 'rasmingiz', 'biografiya']

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(max_length=120 ,widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['username','first_name', 'last_name', 'email', 'password', 'rasmingiz']

    def save(self, commit=True):
        user = super(CustomUserForm, self).save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user
    
class ShartnomaForm(forms.ModelForm):
    boshlanish_sanasi = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    tugash_sanasi = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    class Meta:
        model = Shartnoma
        fields = ('teacher', 'boshlanish_sanasi', 'tugash_sanasi', 'status', 'is_active')

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['ism', 'email', 'telefon', 'xabar']