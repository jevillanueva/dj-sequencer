def has_permission(request):
    return {
        "can_administrate": request.user.has_perm("emission.can_administrate")
    }