from django.urls import reverse
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from autoslug import AutoSlugField
from django.db.models.signals import post_save
from PIL import Image


User = get_user_model()


class UserProfile(models.Model):
    # https://www.devhandbook.com/django/user-profile/
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # Override the save method of the model
    def save(self):
        super().save()

        img = Image.open(self.avatar.path)  # Open image

        # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)  # Resize image
            img.save(self.avatar.path)  # Save it again and override the larger image


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)


# creates table with name 'blog_post'
class Post(models.Model):
    class Meta:
        ordering = ['created_at']
        db_table = 'posts'
    POST_LENGTHS = [
        # first param is stored in DB, second is for display in forms
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large')
    ]
    post_length = models.CharField(max_length=1, choices=POST_LENGTHS)
    # help_text is for 'help' field in forms
    title = models.CharField(max_length=50)
    body = models.TextField()
    # blank will check if input is an empty string
    # can be null
    # Make slug as index
    # slug = models.CharField(max_length=50, unique=True, blank=False, db_index=True)
    # slug = models.SlugField(max_length=50, unique=True, blank=False, db_index=True)
    slug = AutoSlugField(populate_from='title', unique=True, editable=True)
    # many-many relationships are generally defined in model where it is edited
    # default accessed as post_set, Overridden by posts
    # If model is defined later, add '' for name
    categories = models.ManyToManyField('Category', related_name='posts', blank=True)
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True,
                                  help_text='Hold down “Control”, or “Command” on a Mac, to select more than one.')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})

    # can also write methods to override existing model.Model methods

'''
post = Post(........)
post.save()
post.post_length -> 'L'
post.get_post_length_display() -> 'Large'

# add an existing category/ categories
post.categories.add(..)
# create a category adn add it to post
post.categories.create(..)
# set all categories at once
post.categories.set([cat1, cat2. cat3], through_defaults={'created_at': datetime.now()})

post.categories.remove(cat1)
# clear to clear all
post.categories.clear()

Post.objects.filter(categories__name__startswith='World')
category.posts.all()
category.posts.get(..)

We can hAVE INHERITENCE on models as well as Meta Inheritance.
We can have Proxy model as well.

model Manager? -> Each model has one manager and is called 'objects' by default
QuerySet is collection of objects from DB.

Like filter, we also have exclude to exclude.
Querysets are lazy. Only one DB query is used after all filters.

filter will give QuerySet.
get will give single object.
all will give all.
exclude will give excluded QuerySet.

Supported filed lookups

lte <=
gte >=
contains 'LIKE'

In many-many relationships use 1 filter with multiple queries.
(https://apirobot.me/posts/filters-in-django-filtera-b-vs-filtera-filterb)

Blog.objects.filter(entry__headline__contains='Lennon', entry__pub_date__year=2008)
Gives all blogs with entries containing Lennon with publication year 2008

Blog.objects.filter(entry__headline__contains='Lennon').filter(entry__pub_date__year=2008)
First gives me all blog_ids whose entry contains Lennon irrespective of year.
Second on all the above blog_ids it tries to see which blogs were published in 2008

F is used to filter on same table
Post.objects.filter(created_at__gt=F('updated_at'))

Filter queries are AND'ed. To use OR, etc.. we use Q
Q objects
Q(question__startswith='Who') | Q(question__startswith='What') ->
WHERE question LIKE 'Who%' OR question LIKE 'What%'

Post.objects.get(
    Q(title__startswith='Who'),
    Q(created_at=date(2005, 5, 2)) | Q(created_at=date(2005, 5, 6))
)

Uodate
update()
'''


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    # on_delete can be CASCADE, PROTECT, RESTRICT
    # If post is deleted, delete all it's comments
    # Restrict restricts deletion of parent
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    approved = models.BooleanField(default=False)
    commented_at = models.DateTimeField(auto_now_add=True)
