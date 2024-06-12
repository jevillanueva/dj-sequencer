from django.shortcuts import redirect, render, get_object_or_404

def index(request):
    return redirect("emissions:index")