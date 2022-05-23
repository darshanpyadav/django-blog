from django.shortcuts import redirect
from django.views import generic
from blog.models import Category
from category.forms import CategoryModelForm
from django.urls import reverse
from django.contrib import messages


class CategoryListView(generic.ListView):
    model = Category
    template_name = "category/category_list.html"
    context_object_name = "categories"
    success_message = "Category: '{name}' was created successfully"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            {
                "form": CategoryModelForm
            })
        return context_data


def category_create(request):
    if request.method == "POST":
        # pass the request to the form to validate
        form = CategoryModelForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.add_message(request, messages.SUCCESS, f'Category: {category.name} created successfully!')
            return redirect("category:category_list")
        else:
            messages.error(request, f'{form.errors}')
            return redirect("category:category_list")


class CategoryDelete(generic.DeleteView):
    model = Category

    def get_success_url(self):
        messages.error(self.request, "Deleted the category successfully!")
        return reverse("category:category_list")
