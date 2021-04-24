from django import forms
from .models import Profiles

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profiles
        fields = ('first_name','last_name','email','about','category','field_of_interest','profile_pic')