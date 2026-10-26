from functools import wraps # préserver les informations de la fonction décorée
from django.core.exceptions import PermissionDenied #renvoie un statut 403 aux utilisateurs connectés
from django.contrib.auth import get_user_model
from django.http import HttpResponse

User = get_user_model()

def role_required(*allowed_roles):

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request,*args,**kwargs):

            if request.user.is_authenticated and request.user.role in allowed_roles:
                return view_func(request,*args,**kwargs)
            raise PermissionDenied

        return wrapper
    return decorator

