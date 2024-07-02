import socket
from django.http import HttpResponse, JsonResponse
from datetime import datetime


def source_view(request):
    now = datetime.utcnow()
    hostname = socket.gethostname()
    html = "<html><body>It's now {} ({})</body></html>".format(now.isoformat(), hostname)
    return HttpResponse(html)


def health_check_view(request):
    return JsonResponse({"health": "ok v2"})
