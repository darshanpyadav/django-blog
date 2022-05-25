import datetime

from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .forms import PostModelForm, CustomUserCreationForm, CommentModelForm, UserUpdateForm, ProfileUpdateForm
from .models import Post, Comment
from django.views import generic
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.template.defaulttags import register
from django.db.models import Count


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


def index_view(request):
    # return HttpResponse("Hello World!")
    return render(request, "blog/index.html", context={})


class BlogListView(generic.ListView):
    model = Post
    paginate_by = 2
    context_object_name = "posts"
    template_name = "blog/index.html"
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # main_post is the one with most comments in all posts
        popular_posts = Comment.objects.values('post_id').\
            annotate(count=Count('post_id')).\
            order_by('-count')
        if popular_posts:
            popular_post_id = popular_posts[0]["post_id"]
            main_post = Post.objects.get(pk=popular_post_id)
        else:
            main_post = Post.objects.first
        # 2 sub posts are the second and third highest
        context_data.update(
            {
                "main_post": main_post,
                "sub_posts": Post.objects.order_by("-created_at")[:2]
            })
        return context_data


class BlogDetailView(generic.DetailView):
    model = Post
    template_name = "blog/blog_single.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            {
                "comment_form": CommentModelForm
            })
        return context_data

    def post(self, request, *args, **kwargs):
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.get_object()
            if comment.post.user != request.user:
                messages.warning(request, "Your comment has gone for approval to the post publisher. "
                                          "It'll be visible once approved!")
            else:
                comment.approved = True
            comment.user = request.user
            comment.save()
            return redirect("blog:blog_detail", slug=self.get_object().slug)
        else:
            messages.error(request, f'{form.errors}')
            return redirect("blog:blog_list")

    @staticmethod
    @register.filter
    def approved_comments(post_comments):
        return post_comments.filter(approved=True)


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
# class PostCreateView(SuccessMessageMixin, generic.CreateView):
#     form_class = PostModelForm
#     # default is "blog/post_form.html"
#     template_name = "blog/post_create.html"
#     # can define below param instead of get_success_url
#     success_message = "Post with title '{title}' was created successfully"
#
#     def get_success_url(self):
#         return reverse('blog:post_detail', args=(self.object.id,))
#
#     def get_success_message(self, cleaned_data):
#         return self.success_message.format(**cleaned_data)
#
#
# def post_detail(request, pk):
#     post = Post.objects.get(pk=pk)
#     context = {
#         "post": post,
#         "tz": settings.TIME_ZONE
#     }
#     return render(request, "blog/post_detail.html", context=context)


# Phase 4 using slug, add Login
# class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
#     form_class = PostModelForm
#     # default is "blog/post_form.html"
#     template_name = "blog/post_create.html"
#     # can define below param instead of get_success_url
#     success_message = "Post with title '{title}' was created successfully"
#
#     def get_success_url(self):
#         return reverse('blog:post_detail', kwargs={"slug": self.object.slug})
#
#     def get_success_message(self, cleaned_data):
#         return self.success_message.format(**cleaned_data)

# Phase 5 adding user
class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    form_class = PostModelForm
    # default is "blog/post_form.html"
    template_name = "blog/post_create.html"
    # can define below param instead of get_success_url
    success_message = "Post with title '{title}' was created successfully"

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={"slug": self.object.slug})

    def get_success_message(self, cleaned_data):
        return self.success_message.format(**cleaned_data)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return super(PostCreateView, self).form_valid(form)


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {
        "post": post,
        "tz": settings.TIME_ZONE
    }
    return render(request, "blog/post_detail.html", context=context)


# Phase 1
# Phase 2 after adding slug no modification was needed
# Phase 3 Login
# Phase 4 allow detail view only for creators
class PostDetailView(LoginRequiredMixin, generic.DetailView):
    model = Post

    # template_name = "blog/post_detail.html" # -> by default
    # context_object_name = "post"  # ->by default

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"tz": settings.TIME_ZONE})
        return context_data

    def get_queryset(self):
        return Post.objects.filter(slug=self.kwargs["slug"], user=self.request.user)


def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    context = {
        "posts": posts,
        "tz": settings.TIME_ZONE
    }
    return render(request, "blog/post_list.html", context=context)


# class PostListView(LoginRequiredMixin, generic.ListView):
#     model = Post
#     paginate_by = 5
#     context_object_name = "posts"
#     # template_name = "blog/post_list.html"
#     ordering = ['-created_at']


# Phase 2 users can view only their posts
class PostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    paginate_by = 5
    context_object_name = "posts"
    # template_name = "blog/post_list.html"
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.filter(user=user)
        return queryset


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


# No changes were needed after adding slug, other than reverse url
# Only created user can update the post
class PostUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Post
    form_class = PostModelForm
    # default is "blog/post_form.html"
    template_name = "blog/post_update.html"
    # can define below param instead of get_success_url
    success_message = "Post with title '{title}' was updated successfully"

    def get_success_url(self):
        # return reverse('blog:post_detail', args=(self.object.id,))
        return reverse('blog:post_detail', kwargs={"slug": self.object.slug})

    def get_success_message(self, cleaned_data):
        return self.success_message.format(**cleaned_data)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_at = datetime.datetime.utcnow()
        # post.categories.remove()
        # post.tags.remove()
        post.save()
        return super(PostUpdateView, self).form_valid(form)

    def get_object(self, *args, **kwargs):
        obj = super(PostUpdateView, self).get_object(*args, **kwargs)
        if obj.user != self.request.user:
            raise PermissionDenied  # or Http404
        return obj


def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    messages.add_message(request, messages.ERROR, 'Post deletion successful!')
    return redirect('blog:post_list')


# Phase 1
# class PostDeleteView(generic.DeleteView):
#     model = Post
#     success_url = reverse_lazy('blog:post_list')
#     # reverse_lazy should be used if we define attribute
#     # reverse should be used within get_success_utl method


# Phase 2, add message. Slug works without changes
# Phase 3 login
# Phase 4 Only created user can delete the post
class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    """
    DeleteView responds to POST and GET requests, GET request display confirmation template, while POST deletes instance.
    """
    model = Post

    def get_success_url(self):
        messages.error(self.request, "Deleted the post successfully!")
        return reverse("blog:post_list")

    def get_object(self, *args, **kwargs):
        obj = super(PostDeleteView, self).get_object(*args, **kwargs)
        if obj.user != self.request.user:
            raise PermissionDenied  # or Http404
        return obj


class CommentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Comment

    def get_success_url(self):
        messages.error(self.request, "Comment deleted successfully!")
        if self.request.GET.get('redirect') == 'blog':
            return reverse("blog:blog_detail", kwargs={'slug': self.object.post.slug})
        return reverse("blog:post_detail", kwargs={'slug': self.object.post.slug})

    def get_object(self, *args, **kwargs):
        obj = super(CommentDeleteView, self).get_object(*args, **kwargs)
        if obj.user != self.request.user and object.post.user != self.request.user:
            raise PermissionDenied  # or Http404
        return obj


@login_required(login_url="/login/")
def comment_approve(request, pk):
    if request.method == "POST":
        # pass the request to the form to validate
        comment = Comment.objects.get(pk=pk)
        if comment.post.user != request.user:
            raise PermissionDenied  # or Http404
        comment.approved = True
        comment.save()
        messages.success(request, "Comment approved")
        return redirect("blog:post_detail", slug=comment.post.slug)


@login_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.userprofile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')  # Redirect back to profile page

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'user_profile.html', context)
