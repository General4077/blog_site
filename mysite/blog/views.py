import json
from http import HTTPStatus

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Post


@method_decorator(csrf_exempt, name='dispatch') # TODO Fix this. DRF w/ JWT?
class PostView(View):

    def get(self, request, *args, **kwargs):
        qs = Post.objects.values('title', 'content', 'author', 'date_posted')
        data = {'posts': list(qs)}
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                Post(**json.loads(request.body), author=request.user).save()
                return JsonResponse({'message': 'Post saved successfully'}, status=HTTPStatus.CREATED)
            except Exception as e:
                return JsonResponse({'message':'Invalid Request Data'}, status=HTTPStatus.BAD_REQUEST)
        else:
            return JsonResponse({'message': 'Login to post'}, status=HTTPStatus.BAD_REQUEST)
