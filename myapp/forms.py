from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput({'placeholder':'Username'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','first_name','email')

    def clean_password2(self):
        pass1 = self.cleaned_data.get("password1")
        pass2 = self.cleaned_data.get("password2")
        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError("Password does not match")
        return pass2

    def save(self, commit=True):
        userobj = super(RegisterForm, self).save(commit=False)
        userobj.set_password(self.cleaned_data["password2"])
        if commit:
            userobj.save()
        return userobj

class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        uname1 = self.cleaned_data.get("username")
        pass1 = self.cleaned_data.get("password")

        userobj = User.objects.filter(username=uname1).first()

        if not userobj:
            raise forms.ValidationError("Wrong Username")
        else:
            if not userobj.check_password(pass1):
                raise forms.ValidationError("Wrong password")
        return super(LoginForm, self).clean(*args, **kwargs)