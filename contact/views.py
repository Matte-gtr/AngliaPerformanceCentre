from django.shortcuts import render


def blog(request):
    """ a view to display the blog page """
    template = "blog/blog.html"
    context = {
        'title': 'blog',
        'section': 'blog',
    }
    return render(request, template, context)
