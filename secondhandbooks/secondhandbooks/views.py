from django.shortcuts import render


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def error_400(request, exception):
    return render(request, '400.html', status=400)

def error_403(request, exception):
    return render(request, '403.html', status=403)

def error_500(request):
    return render(request, '500.html', status=500)                  