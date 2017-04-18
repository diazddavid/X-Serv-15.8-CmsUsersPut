from django.shortcuts import render

# Create your views here.

from cmsTemp.models import Page
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import logout
from django.shortcuts import redirect

# Create your views here.

def myLogout(request):
    logout(request)
    return redirect(default)

def default(request):
    toReturn = show_content(request)
    if request.method == "GET":
        toReturn += "</br>I have this pages:"
        for page in Page.objects.all():
            toReturn += "</br> <a href=/" + page.name + ">" + page.name + "</a>"
        return HttpResponse(toReturn)

@csrf_exempt
def handlePage(request, rec):
    toReturn = show_content(request)
    if request.method == "GET":
        try:
            page = Page.objects.get(name =  rec)
            return HttpResponse(page.body)
        except ObjectDoesNotExist:
            toReturn += "</br></br>Content: </br>"
            toReturn += rec
            toReturn += " </br> not found, you can add it with a PUT"
            return HttpResponse(toReturn, status = 404)
    elif request.method == "PUT" or request.method == "POST":
        if request.user.is_authenticated():
            try:
                page = Page.objects.get(name =  rec)
                page.body = request.body
                page.save()
            except ObjectDoesNotExist:
                page = Page(name=rec, body=request.body)
                page.save()
                toReturn += "Succesfully added or changed page: " + rec
            return HttpResponse(toReturn)
        else:
            toReturn += "You have to be logged to add content"
            return HttpResponse(toReturn, status=400)
    else:
        return HttpResponse("Method not allowed", status=405)

def show_content(request):
    if request.user.is_authenticated():
        logged = "Logged in as " + request.user.username
        logged += "</br> <a href='/logout/'> LOG OUT</a>."
    else:
        logged = "Not logged in. To add or modify content, please login"
    return logged
