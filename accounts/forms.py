"""Forms for accounts"""
from django import forms


class LoginForm(forms.Form):
    """Class to create form for user."""

    login = forms.CharField(label="Login", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class SubscribeForm(forms.Form):
    """Class to create form for creating user."""

    login = forms.CharField(label="Login", max_length=100)
    last_name = forms.CharField(label="Nom", max_length=120)
    first_name = forms.CharField(label="Prénom", max_length=50)
    email = forms.EmailField(label="E-mail")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirmer", widget=forms.PasswordInput)

    def clean(self):
        """Get cleaned data"""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Les deux mots de passe ne correspondent pas")
