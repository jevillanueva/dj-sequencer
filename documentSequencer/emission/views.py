from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import activate
# Create your views here.
@login_required
def index(request):
    activate('es')
    user = request.user #the user
    email = user.email #their email
    username = user.username #their username
    #  tasks = Task.objects.all()
    # return render(request, "todo/index.html", {"tasks": tasks})
    return render(request, "emission/index.html")