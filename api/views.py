
import requests
from django.http import JsonResponse, Http404
from django.views import View
from django.core.serializers import serialize
import json

from .models import Product

FAKESTORE_API_BASE = 'https://fakestoreapi.com'


class ProductListView(View):
	def get(self, request):
		# Try to get products from database first
		products = list(Product.objects.all().values())
		
		# If no products in database, fetch from API
		if not products:
			resp = requests.get(f'{FAKESTORE_API_BASE}/products')
			return JsonResponse(resp.json(), safe=False)
			
		return JsonResponse(products, safe=False)
	def post(self, request):
		resp = requests.post(f'{FAKESTORE_API_BASE}/products', json=request.POST.dict())
		return JsonResponse(resp.json(), status=resp.status_code, safe=False)


class ProductDetailView(View):
	def get(self, request, pk):
		# Try to get product from database first
		try:
			product = Product.objects.get(fakestore_id=pk)
			return JsonResponse({
				'id': product.fakestore_id,
				'title': product.title,
				'price': float(product.price),
				'description': product.description,
				'category': product.category,
				'image': product.image,
				'rating': {
					'rate': float(product.rating_rate) if product.rating_rate else None,
					'count': product.rating_count
				}
			})
		except Product.DoesNotExist:
			# If not in database, fetch from API
			resp = requests.get(f'{FAKESTORE_API_BASE}/products/{pk}')
			if resp.status_code == 404:
				raise Http404('Product not found')
			return JsonResponse(resp.json(), safe=False)
	def put(self, request, pk):
		resp = requests.put(f'{FAKESTORE_API_BASE}/products/{pk}', json=request.POST.dict())
		return JsonResponse(resp.json(), status=resp.status_code, safe=False)
	def patch(self, request, pk):
		resp = requests.patch(f'{FAKESTORE_API_BASE}/products/{pk}', json=request.POST.dict())
		return JsonResponse(resp.json(), status=resp.status_code, safe=False)
	def delete(self, request, pk):
		resp = requests.delete(f'{FAKESTORE_API_BASE}/products/{pk}')
		return JsonResponse(resp.json(), status=resp.status_code, safe=False)



# CARTS
class CartListView(View):
	def get(self, request):
		resp = requests.get(f'{FAKESTORE_API_BASE}/carts')
		return JsonResponse(resp.json(), safe=False)
	def post(self, request):
		resp = requests.post(f'{FAKESTORE_API_BASE}/carts', json=request.POST.dict())
		return JsonResponse(resp.json(), status=resp.status_code, safe=False)

class CartDetailView(View):
	def get(self, request, pk):
		resp = requests.get(f'{FAKESTORE_API_BASE}/carts/{pk}')
		if resp.status_code == 404:
			raise Http404('Cart not found')
		return JsonResponse(resp.json(), safe=False)
	def put(self, request, pk):
		resp = requests.put(f'{FAKESTORE_API_BASE}/carts/{pk}', json=request.POST.dict())
		return JsonResponse(resp.json(), status=resp.status_code, safe=False)
	def delete(self, request, pk):
		resp = requests.delete(f'{FAKESTORE_API_BASE}/carts/{pk}')
		return JsonResponse(resp.json(), status=resp.status_code, safe=False)

class UserCartListView(View):
	def get(self, request, user_id):
		resp = requests.get(f'{FAKESTORE_API_BASE}/carts/user/{user_id}')
		return JsonResponse(resp.json(), safe=False)

# USERS
class UserListView(View):
	def get(self, request):
		resp = requests.get(f'{FAKESTORE_API_BASE}/users')
		return JsonResponse(resp.json(), safe=False)
	def post(self, request):
		resp = requests.post(f'{FAKESTORE_API_BASE}/users', json=request.POST.dict())
		return JsonResponse(resp.json(), status=resp.status_code, safe=False)

class UserDetailView(View):
	def get(self, request, pk):
		resp = requests.get(f'{FAKESTORE_API_BASE}/users/{pk}')
		if resp.status_code == 404:
			raise Http404('User not found')
		return JsonResponse(resp.json(), safe=False)
	def put(self, request, pk):
		resp = requests.put(f'{FAKESTORE_API_BASE}/users/{pk}', json=request.POST.dict())
		return JsonResponse(resp.json(), status=resp.status_code, safe=False)
	def patch(self, request, pk):
		resp = requests.patch(f'{FAKESTORE_API_BASE}/users/{pk}', json=request.POST.dict())
		return JsonResponse(resp.json(), status=resp.status_code, safe=False)
	def delete(self, request, pk):
		resp = requests.delete(f'{FAKESTORE_API_BASE}/users/{pk}')
		return JsonResponse(resp.json(), status=resp.status_code, safe=False)

# AUTH
class AuthLoginView(View):
	def post(self, request):
		resp = requests.post(f'{FAKESTORE_API_BASE}/auth/login', json=request.POST.dict())
		return JsonResponse(resp.json(), status=resp.status_code, safe=False)
