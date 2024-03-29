from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views import generic
from blog.models import Tag
from .forms import TagModelForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    template_name = "tag/tag_list.html"
    context_object_name = "tags"
    success_message = "Tag: '{name}' was created successfully"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            {
                "form": TagModelForm
            })
        return context_data


@login_required(login_url="/login/")
def tag_create(request):
    if request.method == "POST":
        # pass the request to the form to validate
        form = TagModelForm(request.POST)
        if form.is_valid():
            tag = form.save()
            messages.add_message(request, messages.SUCCESS, f'Tag: {tag.name} created successfully!')
            return redirect("tag:tag_list")
        else:
            messages.error(request, f'{form.errors}')
            return redirect("tag:tag_list")


class TagDetailView(LoginRequiredMixin, generic.DetailView):
    model = Tag
    template_name = "tag/tag_detail.html"


class TagUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Tag
    template_name = "tag/tag_update.html"


class TagDelete(LoginRequiredMixin, generic.DeleteView):
    model = Tag

    def get_success_url(self):
        messages.error(self.request, "Deleted the tag successfully!")
        return reverse("tag:tag_list")
