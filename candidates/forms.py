from django import forms

from candidates.models import Candidate


class CandidateForm(forms.ModelForm):
    username = forms.CharField(help_text='')

    class Meta:
        model = Candidate
        fields = ('photo', 'username', 'first_name', 'last_name', 'email', 'gender', 'about', 'country', 'tags')
        widgets = {'about': forms.Textarea(attrs={'cols': 20, 'rows': 5})}


class LoginForm(forms.Form):
    username = forms.CharField(label='Login')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
