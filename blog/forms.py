from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.exceptions import ValidationError

from .models import Post, Category, Tag
from django import forms


User = get_user_model()


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'post_length',
            'body',
            'categories',
            'tags'
        )

    # Override existing HTML widget using ModelChoiceField
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text='You can select more than one.'
    )

    # tags = forms.ModelMultipleChoiceField(
    #     queryset=Tag.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=False
    # )


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")
        field_classes = {'username': UsernameField}

    email = forms.EmailInput(attrs={'required': 'required'})

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("An user with this email already exists!")
        return email
