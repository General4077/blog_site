
import json
from http import HTTPStatus

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch') # TODO Fix this. DRF w/ JWT?
class Register(View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        try:
            uname = data['username']
            passwd = data['password']
        except KeyError:
            return JsonResponse({'message': f'Username and password are required!'}, status=HTTPStatus.BAD_REQUEST)
        if User.objects.filter(username=uname):
            return JsonResponse({'message': f'Username `{uname}` is not available!'}, status=HTTPStatus.BAD_REQUEST)
        user = User(**data)
        user.set_password(passwd)
        user.save()
        login(request, user)
        return JsonResponse({'message': f"Welcome `{user.get_username()}`"})



@method_decorator(csrf_exempt, name='dispatch')  # TODO Fix this. DRF w/ JWT?
class Login(View):

    
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        try:
            uname = data['username']
            passwd = data['password']
        except KeyError:
            return JsonResponse({'message': f'Username and password are required!'}, status=HTTPStatus.BAD_REQUEST)
        if not request.user.is_authenticated:
            user = authenticate(username=uname, password=passwd)
            if user:
                login(request, user)
                return JsonResponse({"message": f"Welcome `{user.get_username()}`!"})
            else:
                return JsonResponse({"message": "Your credientials don't match our records"}, status=HTTPStatus.UNAUTHORIZED)
        else:
            return JsonResponse({'message': 'You are already logged in!'})

@method_decorator(csrf_exempt, name='dispatch')  # TODO Fix this. DRF w/ JWT?
class Logout(View):

    def post(self, request, *args, **kwargs):
        logout(request)
        return JsonResponse({'message': "Logout Successful"})



class Profile(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return JsonResponse({'username': user.get_username(), 'full_name': user.get_full_name()}) # TODO add user serializer
        else:
            return JsonResponse({'message': 'Login to view profile'})
