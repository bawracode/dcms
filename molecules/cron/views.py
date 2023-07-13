from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
import json
from .models import *


# Create your views here.
def index(request):
    return HttpResponse("cronjob")


def toggle_button(request):
    if request.method == "POST":
        data = json.loads(request.body)

        try:
            cronjob = CronJob.objects.get(id=data["id"])
            cronjob.status = data["status"]
            cronjob.save()
            return JsonResponse({"status":"success"})
        except:
            return JsonResponse({"status":"error"})
