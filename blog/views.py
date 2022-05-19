import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from .forms import PostModelForm
from .models import Post
from django.views import generic
from django.conf import settings


def index_view(request):
    # return HttpResponse("Hello World!")
    return render(request, "blog/index.html", context={})


def contact_view(request):
    return render(request, "contact.html", context={})


def post_create(request):
    # get the post create form
    form = PostModelForm()

    if request.method == "POST":
        # pass the request to the form to validate
        form = PostModelForm(request.POST)
        if form.is_valid():
            form = form.save()
            messages.add_message(request, messages.SUCCESS, 'Post creation successful!')
            return redirect("blog:post_detail", pk=form.id)

    # form is saved if request is POST and then redirected. Else form object/ widgets is sent to HTML to be used
    context = {
        "form": form
    }
    return render(request, "blog/post_create.html", context=context)


# Same thing can be achieved with ClassView
# Phase 1
# class PostsCreateView(generic.CreateView):
#     form_class = PostModelForm
#     # default is "blog/post_form.html"
#     template_name = "blog/post_create.html"
#
#     def get_success_url(self):
#         # messages.success(self.request, "Post creation successful!")
#         # redirect is not supported for get_success_url
#         return reverse("post:post-detail")

# Phase2, using message mixin
# class PostsCreateView(SuccessMessageMixin, generic.CreateView):
#     form_class = PostModelForm
#     # default is "blog/post_form.html"
#     template_name = "blog/post_create.html"
#     # can define below param instead of get_success_url
#     success_url = "/"
#     success_message = "Post with title '{title}' was created successfully"
#
#     def get_success_message(self, cleaned_data):
#         return self.success_message.format(**cleaned_data)

# Phase 3 changing redirect url to show post
class PostCreateView(SuccessMessageMixin, generic.CreateView):
    form_class = PostModelForm
    # default is "blog/post_form.html"
    template_name = "blog/post_create.html"
    # can define below param instead of get_success_url
    success_message = "Post with title '{title}' was created successfully"

    def get_success_url(self):
        return reverse('blog:post_detail', args=(self.object.id,))

    def get_success_message(self, cleaned_data):
        return self.success_message.format(**cleaned_data)


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {
        "post": post,
        "tz": settings.TIME_ZONE
    }
    return render(request, "blog/post_detail.html", context=context)


# Phase 1
class PostDetailView(generic.DetailView):
    model = Post
    # template_name = "blog/post_detail.html" # -> by default
    # context_object_name = "post"  # ->by default

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"tz": settings.TIME_ZONE})
        return context_data


def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    context = {
        "posts": posts,
        "tz": settings.TIME_ZONE
    }
    return render(request, "blog/post_list.html", context=context)


class PostListView(generic.ListView):
    model = Post
    # paginate_by = 10
    context_object_name = "posts"
    # template_name = "blog/post_list.html"
    ordering = ['-created_at']


def post_update(request, pk):
    post = Post.objects.get(pk=pk)
    form = PostModelForm(instance=post)
    if request.method == 'POST':
        form = PostModelForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.updated_at = datetime.datetime.utcnow()
            # post.categories.remove()
            # post.tags.remove()
            post.save()
            form.save_m2m()
            # every time you save a form using commit=False, Django adds a save_m2m()
            # method to your ModelForm subclass.
            messages.add_message(request, messages.SUCCESS, 'Post successfully updated!')
            return redirect("blog:post_detail", pk=post.id)

    context = {
        "form": form
    }
    return render(request, "blog/post_update.html", context=context)


class PostUpdateView(SuccessMessageMixin, generic.UpdateView):
    model = Post
    form_class = PostModelForm
    # default is "blog/post_form.html"
    template_name = "blog/post_update.html"
    # can define below param instead of get_success_url
    success_message = "Post with title '{title}' was updated successfully"

    def get_success_url(self):
        return reverse('blog:post_detail', args=(self.object.id,))

    def get_success_message(self, cleaned_data):
        return self.success_message.format(**cleaned_data)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_at = datetime.datetime.utcnow()
        # post.categories.remove()
        # post.tags.remove()
        post.save()
        return super(PostUpdateView, self).form_valid(form)


def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    messages.add_message(request, messages.ERROR, 'Post deletion successful!')
    return redirect('blog:post_list')
