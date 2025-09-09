from django.http import JsonResponse, Http404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Prefetch
import json

from .models import Product, User, UserAddress, Cart, CartItem

@method_decorator(csrf_exempt, name='dispatch')
class DBProductListView(View):
    def get(self, request):
        """Get all products from the database"""
        products = list(Product.objects.all().values(
            'fakestore_id', 'title', 'price', 'description', 'category', 'image', 'rating_rate', 'rating_count'
        ))
        
        # Format response to match FakeStore API structure
        for product in products:
            product['id'] = product.pop('fakestore_id')
            product['price'] = float(product['price'])
            product['rating'] = {
                'rate': float(product['rating_rate']) if product['rating_rate'] else None,
                'count': product['rating_count']
            }
            del product['rating_rate']
            del product['rating_count']
            
        return JsonResponse(products, safe=False)
    
    def post(self, request):
        """Create a new product in the database"""
        try:
            data = json.loads(request.body)
            rating = data.pop('rating', {})
            
            # Find the highest fakestore_id and add 1
            max_id = Product.objects.all().order_by('-fakestore_id').first()
            new_id = (max_id.fakestore_id + 1) if max_id else 1
            
            product = Product.objects.create(
                fakestore_id=new_id,
                title=data.get('title', ''),
                price=data.get('price', 0),
                description=data.get('description', ''),
                category=data.get('category', ''),
                image=data.get('image', ''),
                rating_rate=rating.get('rate'),
                rating_count=rating.get('count')
            )
            
            # Format response
            response_data = {
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
            }
            
            return JsonResponse(response_data, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class DBProductDetailView(View):
    def get(self, request, pk):
        """Get a product by ID from the database"""
        try:
            product = Product.objects.get(fakestore_id=pk)
            
            # Format response
            response_data = {
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
            }
            
            return JsonResponse(response_data)
        except Product.DoesNotExist:
            raise Http404('Product not found')
    
    def put(self, request, pk):
        """Update a product completely"""
        try:
            product = Product.objects.get(fakestore_id=pk)
            data = json.loads(request.body)
            rating = data.pop('rating', {})
            
            product.title = data.get('title', product.title)
            product.price = data.get('price', product.price)
            product.description = data.get('description', product.description)
            product.category = data.get('category', product.category)
            product.image = data.get('image', product.image)
            product.rating_rate = rating.get('rate', product.rating_rate)
            product.rating_count = rating.get('count', product.rating_count)
            product.save()
            
            # Format response
            response_data = {
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
            }
            
            return JsonResponse(response_data)
        except Product.DoesNotExist:
            raise Http404('Product not found')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    def patch(self, request, pk):
        """Update a product partially"""
        try:
            product = Product.objects.get(fakestore_id=pk)
            data = json.loads(request.body)
            
            if 'title' in data:
                product.title = data['title']
            if 'price' in data:
                product.price = data['price']
            if 'description' in data:
                product.description = data['description']
            if 'category' in data:
                product.category = data['category']
            if 'image' in data:
                product.image = data['image']
            
            if 'rating' in data:
                if 'rate' in data['rating']:
                    product.rating_rate = data['rating']['rate']
                if 'count' in data['rating']:
                    product.rating_count = data['rating']['count']
            
            product.save()
            
            # Format response
            response_data = {
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
            }
            
            return JsonResponse(response_data)
        except Product.DoesNotExist:
            raise Http404('Product not found')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    def delete(self, request, pk):
        """Delete a product"""
        try:
            product = Product.objects.get(fakestore_id=pk)
            product_data = {
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
            }
            product.delete()
            return JsonResponse(product_data)
        except Product.DoesNotExist:
            raise Http404('Product not found')
