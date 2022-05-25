from django.contrib import admin
from .models import Post, Category, Tag, UserProfile
from django.contrib.auth.models import Group


class PostAdmin(admin.ModelAdmin):
    # fields are used to manipulate the fields in creation field
    # fields = (
    #     'title',
    #     'post_length',
    #     'slug',
    #     'body'
    # )
    # fields are used to manipulate the display view
    list_display = ['title', 'slug', 'created_at']
    list_display_links = ['title']
    # list_editable = ['slug']
    list_filter = ['created_at']
    search_fields = ['title']


admin.site.unregister(Group)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(UserProfile)
