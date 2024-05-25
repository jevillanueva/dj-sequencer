from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.translation import activate

from .forms import EmissionForm
from .models import Emission


# Create your views here.
@login_required
def index(request):
    activate("es")
    user = request.user  # the user
    email = user.email  # their email
    username = user.username  # their username
    emissions = Emission.objects.filter()
    return render(request, "emission/index.html", {"emissions": emissions})


@login_required
# @permission_required('todo.can_view_tasks', raise_exception=True)
def new(request):
    if request.method == "POST":
        form = Emission(request.POST)
        if form.is_valid():
            task = form.save()
            return redirect("emissions:index")
    else:
        form = EmissionForm()
    return render(request, "emission/new.html", {"form": form, "emission": None})
