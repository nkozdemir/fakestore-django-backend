import requests
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

# FakeStore API base URL
FAKESTORE_API_BASE = 'https://fakestoreapi.com'

@method_decorator(csrf_exempt, name='dispatch')
class AuthLoginView(View):
    def post(self, request):
        """Login a user by proxying to FakeStore API"""
        try:
            # Get the login data from the request
            data = json.loads(request.body)
            
            # Forward the request to FakeStore API
            response = requests.post(
                f'{FAKESTORE_API_BASE}/auth/login', 
                json=data
            )
            
            # Return the response from FakeStore API
            return JsonResponse(response.json(), status=response.status_code, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
