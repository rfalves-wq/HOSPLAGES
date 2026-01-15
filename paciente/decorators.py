from django.contrib.auth.decorators import user_passes_test

def grupo_requerido(grupos):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and (
                request.user.is_superuser or
                request.user.groups.filter(name__in=grupos).exists()
            ):
                return view_func(request, *args, **kwargs)
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("Acesso negado.")
        return _wrapped_view
    return decorator
