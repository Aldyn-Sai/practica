from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def login_required_message(function=None):
  
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.info(request, 'Для доступа к этой странице необходимо войти в систему')
                return redirect('login')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    
    if function:
        return decorator(function)
    return decorator