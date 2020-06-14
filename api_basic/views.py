from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view # Commit 4 - All the packages from here are used for the Browseable REST API
from rest_framework.response import Response
from rest_framework import status

# from django.views.decorators.csrf import csrf_exempt <-- Needed that the API works without CSRF Token when not using api_view decorator, not safe for production!

from .models import Article
from .serializers import ArticleSerializer

# Create your views here.

@api_view(['GET', 'POST']) # Specify what is possible to do in this function based api view
def article_list(request):

    if request.method == 'GET': # Returns all Articles
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data) 

    elif request.method == 'POST': # Creates new article
        # data = JSONParser().parse(request) <-- This is now not needed anymore with the api_view decorator
        serializer = ArticleSerializer(data=request.data) # Now it`s request.data instead of "data=data"

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) # Status: Created - Commit 4: New Status from REST Framework
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # Status: Failure


@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, pk):
    try:  # Checks if article exists
        article = Article.objects.get(pk=pk)

    except Article.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET': # Get data from one Article
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT': # Update Data from existing article
        # data = JSONParser().parse(request) <-- This is now not needed anymore with the api_view decorator
        serializer = ArticleSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE': # Delete Article
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)