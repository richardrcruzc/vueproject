def is_admin(request):
    return request.user.groups.filter(name__in=['admin']).exists()