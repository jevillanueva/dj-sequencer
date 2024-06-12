def has_permission(request):
    return {
        "can_receive": request.user.has_perm("emission.can_receive")
    }