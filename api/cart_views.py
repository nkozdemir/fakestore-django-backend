from django.http import JsonResponse, Http404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.db.models import Prefetch

from .models import Cart, CartItem, User, Product

@method_decorator(csrf_exempt, name='dispatch')
class DBCartListView(View):
    def get(self, request):
        """Get all carts from the database"""
        carts = Cart.objects.select_related('user').prefetch_related(
            Prefetch('items', queryset=CartItem.objects.select_related('product'))
        ).all()
        
        result = []
        for cart in carts:
            cart_data = {
                'id': cart.fakestore_id,
                'userId': cart.user.fakestore_id,
                'date': cart.date.isoformat() if cart.date else None,
                'products': []
            }
            
            # Add products in cart
            for item in cart.items.all():
                cart_data['products'].append({
                    'productId': item.product.fakestore_id,
                    'quantity': item.quantity
                })
                
            result.append(cart_data)
            
        return JsonResponse(result, safe=False)
    
    def post(self, request):
        """Create a new cart in the database"""
        try:
            data = json.loads(request.body)
            
            # Find the highest fakestore_id and add 1
            max_id = Cart.objects.all().order_by('-fakestore_id').first()
            new_id = (max_id.fakestore_id + 1) if max_id else 1
            
            # Get user or return error
            try:
                user = User.objects.get(fakestore_id=data.get('userId'))
            except User.DoesNotExist:
                return JsonResponse({'error': f"User with ID {data.get('userId')} not found"}, status=400)
            
            # Create cart
            cart = Cart.objects.create(
                fakestore_id=new_id,
                user=user,
                date=data.get('date')
            )
            
            # Add products
            for product_data in data.get('products', []):
                try:
                    product = Product.objects.get(fakestore_id=product_data.get('productId'))
                    CartItem.objects.create(
                        cart=cart,
                        product=product,
                        quantity=product_data.get('quantity', 1)
                    )
                except Product.DoesNotExist:
                    return JsonResponse({'error': f"Product with ID {product_data.get('productId')} not found"}, status=400)
            
            # Format response
            response_data = {
                'id': cart.fakestore_id,
                'userId': cart.user.fakestore_id,
                'date': cart.date.isoformat() if cart.date else None,
                'products': []
            }
            
            # Add products to response
            for item in cart.items.all():
                response_data['products'].append({
                    'productId': item.product.fakestore_id,
                    'quantity': item.quantity
                })
            
            return JsonResponse(response_data, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class DBCartDetailView(View):
    def get(self, request, pk):
        """Get a cart by ID from the database"""
        try:
            cart = Cart.objects.select_related('user').prefetch_related(
                Prefetch('items', queryset=CartItem.objects.select_related('product'))
            ).get(fakestore_id=pk)
            
            # Format response
            response_data = {
                'id': cart.fakestore_id,
                'userId': cart.user.fakestore_id,
                'date': cart.date.isoformat() if cart.date else None,
                'products': []
            }
            
            # Add products to response
            for item in cart.items.all():
                response_data['products'].append({
                    'productId': item.product.fakestore_id,
                    'quantity': item.quantity
                })
            
            return JsonResponse(response_data)
        except Cart.DoesNotExist:
            raise Http404('Cart not found')
            
    def put(self, request, pk):
        """Update a cart completely"""
        try:
            cart = Cart.objects.get(fakestore_id=pk)
            data = json.loads(request.body)
            
            # Update cart fields if provided
            if 'userId' in data:
                try:
                    cart.user = User.objects.get(fakestore_id=data.get('userId'))
                except User.DoesNotExist:
                    return JsonResponse({'error': f"User with ID {data.get('userId')} not found"}, status=400)
                
            if 'date' in data:
                cart.date = data.get('date')
                
            cart.save()
            
            # Update products if provided
            if 'products' in data:
                # Delete existing items
                cart.items.all().delete()
                
                # Add new items
                for product_data in data.get('products', []):
                    try:
                        product = Product.objects.get(fakestore_id=product_data.get('productId'))
                        CartItem.objects.create(
                            cart=cart,
                            product=product,
                            quantity=product_data.get('quantity', 1)
                        )
                    except Product.DoesNotExist:
                        return JsonResponse({'error': f"Product with ID {product_data.get('productId')} not found"}, status=400)
            
            # Format response
            response_data = {
                'id': cart.fakestore_id,
                'userId': cart.user.fakestore_id,
                'date': cart.date.isoformat() if cart.date else None,
                'products': []
            }
            
            # Add products to response
            for item in cart.items.all():
                response_data['products'].append({
                    'productId': item.product.fakestore_id,
                    'quantity': item.quantity
                })
            
            return JsonResponse(response_data)
        except Cart.DoesNotExist:
            raise Http404('Cart not found')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    def patch(self, request, pk):
        """Partially update a cart (add/update/remove products, change user/date)"""
        try:
            cart = Cart.objects.get(fakestore_id=pk)
            data = json.loads(request.body)

            # Change user if provided
            if 'userId' in data:
                try:
                    cart.user = User.objects.get(fakestore_id=data.get('userId'))
                except User.DoesNotExist:
                    return JsonResponse({'error': f"User with ID {data.get('userId')} not found"}, status=400)

            # Change date if provided
            if 'date' in data:
                cart.date = data.get('date')

            # Operations on products
            # Expected structure (any subset):
            # {
            #   "add": [{"productId": 1, "quantity": 2}, ...],
            #   "update": [{"productId": 1, "quantity": 5}, ...],
            #   "remove": [3,4]
            # }
            # If a product is added that already exists, quantity is incremented unless also in update.

            # Helper: build lookup of existing items
            existing_items = {ci.product.fakestore_id: ci for ci in cart.items.select_related('product').all()}

            # Handle add
            for prod in data.get('add', []) or []:
                pid = prod.get('productId')
                qty = prod.get('quantity', 1)
                if pid is None:
                    continue
                try:
                    product = Product.objects.get(fakestore_id=pid)
                except Product.DoesNotExist:
                    return JsonResponse({'error': f"Product with ID {pid} not found"}, status=400)
                if pid in existing_items:
                    existing_items[pid].quantity += qty
                    existing_items[pid].save()
                else:
                    CartItem.objects.create(cart=cart, product=product, quantity=qty)

            # Handle update (set quantity)
            for prod in data.get('update', []) or []:
                pid = prod.get('productId')
                if pid is None:
                    continue
                qty = prod.get('quantity')
                if qty is None or qty < 0:
                    return JsonResponse({'error': f"Invalid quantity for product {pid}"}, status=400)
                # Create if not exists (upsert semantics)
                try:
                    product = Product.objects.get(fakestore_id=pid)
                except Product.DoesNotExist:
                    return JsonResponse({'error': f"Product with ID {pid} not found"}, status=400)
                item = existing_items.get(pid)
                if item:
                    item.quantity = qty
                    item.save()
                else:
                    CartItem.objects.create(cart=cart, product=product, quantity=qty)

            # Handle remove
            for pid in data.get('remove', []) or []:
                if pid in existing_items:
                    existing_items[pid].delete()

            cart.save()

            # Response
            response_data = {
                'id': cart.fakestore_id,
                'userId': cart.user.fakestore_id,
                'date': cart.date.isoformat() if cart.date else None,
                'products': []
            }
            for item in cart.items.select_related('product').all():
                response_data['products'].append({
                    'productId': item.product.fakestore_id,
                    'quantity': item.quantity
                })
            return JsonResponse(response_data)
        except Cart.DoesNotExist:
            raise Http404('Cart not found')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    def delete(self, request, pk):
        """Delete a cart"""
        try:
            cart = Cart.objects.get(fakestore_id=pk)
            
            # Prepare response before deletion
            response_data = {
                'id': cart.fakestore_id,
                'userId': cart.user.fakestore_id,
            }
            
            # Delete cart (this will cascade delete items as well)
            cart.delete()
            
            return JsonResponse(response_data)
        except Cart.DoesNotExist:
            raise Http404('Cart not found')

@method_decorator(csrf_exempt, name='dispatch')
class DBUserCartListView(View):
    def get(self, request, user_id):
        """Get carts for a specific user from the database"""
        try:
            user = User.objects.get(fakestore_id=user_id)
            
            carts = Cart.objects.filter(user=user).prefetch_related(
                Prefetch('items', queryset=CartItem.objects.select_related('product'))
            )
            
            result = []
            for cart in carts:
                cart_data = {
                    'id': cart.fakestore_id,
                    'userId': cart.user.fakestore_id,
                    'date': cart.date.isoformat() if cart.date else None,
                    'products': []
                }
                
                # Add products in cart
                for item in cart.items.all():
                    cart_data['products'].append({
                        'productId': item.product.fakestore_id,
                        'quantity': item.quantity
                    })
                    
                result.append(cart_data)
                
            return JsonResponse(result, safe=False)
        except User.DoesNotExist:
            raise Http404('User not found')
