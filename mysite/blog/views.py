from django.http import JsonResponse
from django.views import View
from .models import Post

class PostView(View):

    def get(self, request, *args, **kwargs):
        qs = Post.objects.values('title', 'content', 'author', 'date_posted')
        data = {'posts': list(qs)}
        return JsonResponse(data)