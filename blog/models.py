from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


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
    body = models.TextField(help_text='Enter post text here')
    # blank will check if input is an empty string
    # can be null
    slug = models.CharField(max_length=50, unique=True, blank=False)
    # many-many relationships are generally defined in model where it is edited
    # default accessed as post_set, Overridden by posts
    # If model is defined later, add '' for name
    categories = models.ManyToManyField('Category', related_name='posts', blank=True)
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True,
                                  help_text='Hold down “Control”, or “Command” on a Mac, to select more than one.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

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
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Comment(models.Model):
    # on_delete can be CASCADE, PROTECT, RESTRICT
    # If post is deleted, delete all it's comments
    # Restrict restricts deletion of parent
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(help_text='Enter post text here')
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    approved = models.BooleanField(default=False)
    commented_at = models.DateTimeField(auto_now_add=True)