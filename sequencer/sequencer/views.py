from django.shortcuts import redirect, render, get_object_or_404

def index(request):
    # if user authenticated
    if request.user.is_authenticated:
        return redirect("emissions:index")
    else:
        return redirect("login")