import socket
from django.http import HttpResponse
from .models import Counter
from time import sleep
from .tasks import s3_file_uploader, counter_checker, counter_checker_first

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


def upload_file_view(request):
    filename = request.GET.get("filename")
    content = request.GET.get("content")
    s3_file_uploader.delay(filename=filename, content=content)
    html = f"""
    <html><body>
    Uploading in background, file {filename} with content: {content}
    </body></html>
    """
    return HttpResponse(html)


def counter_checker_view(request):
    timer = request.GET.get("timer")
    task = counter_checker.delay(timer)
    while (task.status != "SUCCESS"):
        sleep(1)
    result = task.get()
    html = f"""
    <html><body>
    Got Result from background task: {result}
    </body></html>
    """
    return HttpResponse(html)

def counter_checker_first_view(request):
    timer = request.GET.get("timer")
    task = counter_checker_first.delay(timer)
    while (task.status != "SUCCESS"):
        sleep(1)
    result = task.get()
    html = f"""
    <html><body>
    Got Result from background task: {result}
    </body></html>
    """
    return HttpResponse(html)
