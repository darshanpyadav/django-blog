from .models import Post, Category, Tag
from django import forms


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
