from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)


from django import forms
from django.contrib.auth import get_user_model


class SignupForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password")
        p2 = cleaned.get("confirm_password")

        if p1 and p2 and p1 != p2:
            self.add_error("confirm_password", "Passwords do not match")

        return cleaned

    def clean_email(self):
        email = self.cleaned_data.get("email")
        User = get_user_model()

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")

        return email