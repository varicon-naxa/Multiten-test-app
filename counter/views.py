from django.shortcuts import render
import socket
from django.http import HttpResponse
from .models import Counter

# Create your views here.

def counter_view(request):
    hostname = socket.gethostname()
    Counter.objects.create()
    total_counts = Counter.objects.count()
    query = Counter.objects.order_by("-accessed_timestamp")[:10]
    html = """
    <html><body>
    <h5> Hostname: {} </h5>
    <h4> Total Counts: {} <h4>
    <ol>
        {}
    </ol>
    """.format(
        hostname,
        total_counts,
        "\n".join(
            [f"<li>{item}</li>" for item in query]
        )
    )
    return HttpResponse(html)
