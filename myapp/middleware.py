# myapp/middleware.py

from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of URLs that should be accessible without login
        public_urls = [reverse('login'), reverse('register'), '/admin/']
        
        if not request.user.is_authenticated:
            if request.path not in public_urls and not request.path.startswith('/admin/'):
                return redirect('login')
        
        return self.get_response(request)