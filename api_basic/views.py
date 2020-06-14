from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser

from django.views.decorators.csrf import csrf_exempt # Needed that the API works without CSRF Token, not safe for production!

from .models import Article
from .serializers import ArticleSerializer

# Create your views here.

@csrf_exempt # Needed that the API works without CSRF Token, not safe for production!
def article_list(request):

    if request.method == 'GET': # Returns all Articles
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return JsonResponse(serializer.data, safe=False) 

    elif request.method == 'POST': # Creates new article
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201) # Status: Created
        return JsonResponse(serializer.errors, status=400) # Status: Failure


@csrf_exempt # Needed that the API works without CSRF Token, not safe for production!
def article_detail(request, pk):
    try:  # Checks if article exists
        article = Article.objects.get(pk=pk)

    except Article.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET': # Get data from one Article
        serializer = ArticleSerializer(article)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT': # Update Data from existing article
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(article, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE': # Delete Article
        article.delete()
        return HttpResponse(status=204)