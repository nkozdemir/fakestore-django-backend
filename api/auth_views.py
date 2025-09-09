from django.http import JsonResponse, Http404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from .models import User

@method_decorator(csrf_exempt, name='dispatch')
class DBAuthLoginView(View):
    def post(self, request):
        """Login a user and return a token"""
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            # Simple auth - in a real app, use proper auth with hashed passwords
            try:
                user = User.objects.get(username=username, password=password)
                
                # Return a simple token with user info (in a real app, use JWT or similar)
                return JsonResponse({
                    'token': f'fake_token_{user.fakestore_id}',
                    'userId': user.fakestore_id
                })
            except User.DoesNotExist:
                return JsonResponse({
                    'error': 'Invalid username or password'
                }, status=401)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
