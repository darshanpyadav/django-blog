from .models import Tag


def categories(request):
    return {
        'tags': Tag.objects.order_by('id')
    }
