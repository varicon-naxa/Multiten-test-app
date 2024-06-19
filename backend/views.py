import socket
from django.http import HttpResponse
from datetime import datetime


def source_view(request):
    now = datetime.utcnow()
    hostname = socket.gethostname()
    html = "<html><body>It's now {} ({})</body></html>".format(now.isoformat(), hostname)
    return HttpResponse(html)
