from django.core.exceptions import ValidationError
from django import forms
from .models import Account, CommentAndRating, UserProfile
from captcha.fields import CaptchaField


class RegistrationForm(forms.ModelForm):
    captcha = CaptchaField()
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Type your password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Retype your password'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email',
                  'phone_number', 'username', 'password', 'captcha']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('passwords does not match')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserForm(forms.ModelForm):
    class Meta:
        email = forms.EmailField(max_length=100)
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number']

        def __init__(self, *args, **kwargs):
            super(UserForm, self).__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    profil_picture = forms.ImageField(required=False, error_messages={
                                      'invalid': ("image files only")}, widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ['address_line_1', 'address_line_2',
                  'city', 'state', 'country', 'profil_picture']

        def __init__(self, *args, **kwargs):
            super(UserProfileForm, self).__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-control'


class CommentswithRatings(forms.ModelForm):
    rating = forms.IntegerField(min_value=1)

    class Meta:
        model = CommentAndRating
        fields = ['review', 'rating']
