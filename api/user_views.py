from django.http import JsonResponse, Http404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from .models import User, UserAddress 

@method_decorator(csrf_exempt, name='dispatch')
class DBUserListView(View):
    def get(self, request):
        """Get all users from the database"""
        users = User.objects.select_related('address').all()
        result = []
        
        for user in users:
            user_data = {
                'id': user.fakestore_id,
                'email': user.email,
                'username': user.username,
                # Do not expose password hashes
                'name': {
                    'firstname': user.name_firstname,
                    'lastname': user.name_lastname
                },
                'address': {
                    'city': user.address.city,
                    'street': user.address.street,
                    'number': user.address.number,
                    'zipcode': user.address.zipcode,
                    'geolocation': {
                        'lat': user.address.geolocation_lat,
                        'long': user.address.geolocation_long
                    }
                },
                'phone': user.phone
            }
            result.append(user_data)
            
        return JsonResponse(result, safe=False)
    
    def post(self, request):
        """Create a new user in the database"""
        try:
            data = json.loads(request.body)
            
            # Find the highest fakestore_id and add 1
            max_id = User.objects.all().order_by('-fakestore_id').first()
            new_id = (max_id.fakestore_id + 1) if max_id else 1
            
            # Create address
            address_data = data.get('address', {})
            geolocation = address_data.get('geolocation', {})
            
            address = UserAddress.objects.create(
                geolocation_lat=geolocation.get('lat'),
                geolocation_long=geolocation.get('long'),
                city=address_data.get('city', ''),
                street=address_data.get('street', ''),
                number=address_data.get('number', 0),
                zipcode=address_data.get('zipcode', '')
            )
            
            # Create user
            name = data.get('name', {})
            user = User.objects.create_user(
                username=data.get('username', ''),
                email=data.get('email', ''),
                password=data.get('password', ''),
                first_name=name.get('firstname', ''),
                last_name=name.get('lastname', ''),
            )
            user.fakestore_id = new_id
            user.address = address
            user.phone = data.get('phone', '')
            user.name_firstname = name.get('firstname', '')
            user.name_lastname = name.get('lastname', '')
            user.save()
            
            # Format response
            response_data = {
                'id': user.fakestore_id,
                'email': user.email,
                'username': user.username,
                # Do not expose password hashes
                'name': {
                    'firstname': user.name_firstname,
                    'lastname': user.name_lastname
                },
                'address': {
                    'city': user.address.city,
                    'street': user.address.street,
                    'number': user.address.number,
                    'zipcode': user.address.zipcode,
                    'geolocation': {
                        'lat': user.address.geolocation_lat,
                        'long': user.address.geolocation_long
                    }
                },
                'phone': user.phone
            }
            
            return JsonResponse(response_data, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class DBUserDetailView(View):
    def get(self, request, pk):
        """Get a user by ID from the database"""
        try:
            user = User.objects.select_related('address').get(fakestore_id=pk)
            
            # Format response
            response_data = {
                'id': user.fakestore_id,
                'email': user.email,
                'username': user.username,
                'password': user.password,
                'name': {
                    'firstname': user.name_firstname,
                    'lastname': user.name_lastname
                },
                'address': {
                    'city': user.address.city,
                    'street': user.address.street,
                    'number': user.address.number,
                    'zipcode': user.address.zipcode,
                    'geolocation': {
                        'lat': user.address.geolocation_lat,
                        'long': user.address.geolocation_long
                    }
                },
                'phone': user.phone
            }
            
            return JsonResponse(response_data)
        except User.DoesNotExist:
            raise Http404('User not found')
            
    def put(self, request, pk):
        """Update a user completely"""
        try:
            user = User.objects.select_related('address').get(fakestore_id=pk)
            data = json.loads(request.body)
            
            # Update user fields
            name = data.get('name', {})
            user.email = data.get('email', user.email)
            user.username = data.get('username', user.username)
            if 'password' in data:
                user.set_password(data['password'])
            user.name_firstname = name.get('firstname', user.name_firstname)
            user.name_lastname = name.get('lastname', user.name_lastname)
            user.phone = data.get('phone', user.phone)
            
            # Update address fields
            address_data = data.get('address', {})
            geolocation = address_data.get('geolocation', {})
            user.address.city = address_data.get('city', user.address.city)
            user.address.street = address_data.get('street', user.address.street)
            user.address.number = address_data.get('number', user.address.number)
            user.address.zipcode = address_data.get('zipcode', user.address.zipcode)
            user.address.geolocation_lat = geolocation.get('lat', user.address.geolocation_lat)
            user.address.geolocation_long = geolocation.get('long', user.address.geolocation_long)
            
            # Save changes
            user.address.save()
            user.save()
            
            # Format response
            response_data = {
                'id': user.fakestore_id,
                'email': user.email,
                'username': user.username,
                # Do not expose password hashes
                'name': {
                    'firstname': user.name_firstname,
                    'lastname': user.name_lastname
                },
                'address': {
                    'city': user.address.city,
                    'street': user.address.street,
                    'number': user.address.number,
                    'zipcode': user.address.zipcode,
                    'geolocation': {
                        'lat': user.address.geolocation_lat,
                        'long': user.address.geolocation_long
                    }
                },
                'phone': user.phone
            }
            
            return JsonResponse(response_data)
        except User.DoesNotExist:
            raise Http404('User not found')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    def patch(self, request, pk):
        """Partially update a user (only provided fields)"""
        try:
            user = User.objects.select_related('address').get(fakestore_id=pk)
            data = json.loads(request.body)

            # Update simple scalar fields if present
            if 'email' in data:
                user.email = data['email']
            if 'username' in data:
                user.username = data['username']
            if 'password' in data:
                user.set_password(data['password'])
            if 'phone' in data:
                user.phone = data['phone']

            # Name (nested)
            if 'name' in data:
                name = data['name'] or {}
                if 'firstname' in name:
                    user.name_firstname = name['firstname']
                if 'lastname' in name:
                    user.name_lastname = name['lastname']

            # Address (nested)
            if 'address' in data:
                addr_payload = data['address'] or {}
                address = user.address
                # If user has no address yet and payload has something, create one
                if not address:
                    address = UserAddress.objects.create()
                    user.address = address
                if 'city' in addr_payload:
                    address.city = addr_payload['city']
                if 'street' in addr_payload:
                    address.street = addr_payload['street']
                if 'number' in addr_payload:
                    address.number = addr_payload['number']
                if 'zipcode' in addr_payload:
                    address.zipcode = addr_payload['zipcode']
                if 'geolocation' in addr_payload:
                    geo = addr_payload['geolocation'] or {}
                    if 'lat' in geo:
                        address.geolocation_lat = geo['lat']
                    if 'long' in geo:
                        address.geolocation_long = geo['long']
                address.save()

            user.save()

            response_data = {
                'id': user.fakestore_id,
                'email': user.email,
                'username': user.username,
                'name': {
                    'firstname': user.name_firstname,
                    'lastname': user.name_lastname
                },
                'address': {
                    'city': user.address.city if user.address else None,
                    'street': user.address.street if user.address else None,
                    'number': user.address.number if user.address else None,
                    'zipcode': user.address.zipcode if user.address else None,
                    'geolocation': {
                        'lat': user.address.geolocation_lat if user.address else None,
                        'long': user.address.geolocation_long if user.address else None
                    } if user.address else None
                } if user.address else None,
                'phone': user.phone
            }
            return JsonResponse(response_data)
        except User.DoesNotExist:
            raise Http404('User not found')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    def delete(self, request, pk):
        """Delete a user"""
        try:
            user = User.objects.get(fakestore_id=pk)
            
            # Prepare response before deletion
            response_data = {
                'id': user.fakestore_id,
                'email': user.email,
                'username': user.username,
            }
            
            # Get the address to delete separately
            address = user.address
            
            # Delete user
            user.delete()
            
            # Delete the address
            address.delete()
            
            return JsonResponse(response_data)
        except User.DoesNotExist:
            raise Http404('User not found')
