from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.translation import activate

from .forms import EmissionForm
from .models import Emission, UserDepartment


# Create your views here.
@login_required
def index(request):
    activate("es")
    user = request.user  # the user
    email = user.email  # their email
    username = user.username  # their username
    emissions = Emission.objects.filter()
    user_departments = UserDepartment.objects.filter(user=user)
    return render(
        request,
        "emission/index.html",
        {"emissions": emissions, "user_departments": user_departments},
    )


@login_required
# @permission_required('todo.can_view_tasks', raise_exception=True)
def new(request):
    if request.method == "POST":
        form = EmissionForm(request.POST,user=request.user)
        if form.is_valid():
            emission = form.save()
            return redirect("emissions:index")
    else:
        form = EmissionForm(user=request.user)
    return render(request, "emission/new.html", {"form": form, "emission": None})


@login_required
def user_department(request):
    activate("es")
    user = request.user  # the user
    email = user.email  # their email
    username = user.username  # their username
    user_departments = UserDepartment.objects.filter()
    return render(
        request, "user_department/index.html", {"user_departments": user_departments}
    )
