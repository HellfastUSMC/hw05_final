from django.shortcuts import render


def page_not_found(request, exception):
    template = 'core/404.html'
    context = {
        'path': request.path,
        'exception': exception
    }
    return render(request, template, context, status=404)


def permission_denied_view(request, exception):
    template = 'core/403.html'
    context = {
        'path': request.path,
        'exception': exception
    }
    return render(request, template, context, status=403)


def server_error(request):
    template = 'core/500.html'
    context = {
        'path': request.path,
    }
    return render(request, template, context, status=500)
