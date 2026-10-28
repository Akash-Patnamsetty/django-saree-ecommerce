from functools import wraps

from django.http import HttpResponseForbidden
from django.shortcuts import redirect

from .models import Users


def role_required(*allowed_roles):
    """Allow access only to logged-in, active users whose role is in allowed_roles.
    The user is reloaded from the database on every request, so a demoted or
    deactivated account loses access immediately."""

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user_id = request.session.get("user_id")
            if not user_id:
                return redirect("login")

            user = Users.objects.filter(pk=user_id, is_active=True).first()
            if user is None:
                request.session.flush()
                return redirect("login")
               
            if user.must_change_password:
                return redirect("force_password_change")
               
            if user.role not in allowed_roles:
                return HttpResponseForbidden("You do not have permission to view this page.")

            request.current_user = user
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


staff_required = role_required(Users.ROLE_STAFF, Users.ROLE_ADMIN)
admin_required = role_required(Users.ROLE_ADMIN)