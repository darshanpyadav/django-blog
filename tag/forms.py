from django import forms
from blog.models import Tag


class TagModelForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = (
            'name',
        )
