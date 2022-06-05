from datetime import datetime
import json
from http import HTTPStatus

from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Post


@method_decorator(csrf_exempt, name='dispatch') # TODO Fix this. DRF w/ JWT?
class PostView(View):

    def get(self, request, *args, id_=None, **kwargs):
        paginate = bool(int(request.GET.get('paginate', 1)))
        page_size = int(request.GET.get('page_size', 1))
        page_offset = int(request.GET.get('page_offset', 1))
        if not id_ and not paginate:
            qs = Post.objects.order_by('date_posted')
        elif not id_:
            qs = Paginator(Post.objects.order_by('date_posted').all(), page_size).get_page(page_offset).object_list
        else:
            qs = Post.objects.filter(pk=id_)
        data = {'posts': list(qs.values('title', 'content', 'author', 'date_posted', 'last_updated'))}
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'message': 'Login to post'}, status=HTTPStatus.BAD_REQUEST)
        try:
            Post(**json.loads(request.body), author=request.user).save()
            return JsonResponse({'message': 'Post saved successfully'}, status=HTTPStatus.CREATED)
        except IntegrityError:
            return JsonResponse({'message': 'A post with that title already exists!'}, status=HTTPStatus.BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'message':'Invalid Request Data'}, status=HTTPStatus.BAD_REQUEST)
            


    def put(self, request, *args, id_, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'message': 'Login to update a post'}, status=HTTPStatus.BAD_REQUEST)
        post = Post.objects.filter(pk=id_).first()
        try:
            if not post.author == request.user:
                return JsonResponse({'message': 'Only the author can edit a post!'}, status=HTTPStatus.UNAUTHORIZED)
        except TypeError:
            return JsonResponse({'message': 'Post not found'}, status=HTTPStatus.BAD_REQUEST)
        data = json.loads(request.body)
        post.title = data.get('title',post.title)
        post.content = data.get('content', post.content)
        post.last_updated = datetime.now()
        post.save()
        return JsonResponse({'message': 'Updated'}, status=HTTPStatus.ACCEPTED)

    def delete(self, request, *args, id_, **kwargs):
        post = Post.objects.filter(pk=id_).first()
        if request.user.is_authenticated and (request.user.is_superuser or request.user == post.author):
            post.delete()
            return JsonResponse({'message': 'Deleted'}, status=HTTPStatus.ACCEPTED)
        return JsonResponse({'message': 'Unauthorized'}, status=HTTPStatus.UNAUTHORIZED)
