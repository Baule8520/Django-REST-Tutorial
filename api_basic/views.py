from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view # Commit 4 - The 3 packages down from here are used for the Browseable REST API
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView # Commit 5 - To use Class Based Views, see classes ArticleAPIView & ArticleAPIDetail
from rest_framework import generics, mixins # Commit 6 - To use Generic API Views
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication # Commit 7 - 3 Types of Authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets # Commit 8 - Using ViewSets
from django.shortcuts import get_object_or_404

# from django.views.decorators.csrf import csrf_exempt <-- Needed that the API works without CSRF Token when not using api_view decorator, not safe for production!

from .models import Article
from .serializers import ArticleSerializer


######## Function Based API Views ########


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


######## Class Based API Views ########


class ArticleAPIView(APIView): # Like the "def article_list(request):" above but with less code

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data) 

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleAPIDetail(APIView): # Like the "def article_detail(request, pk):" above but with less code

    def get_object(self, id):
        try:
            return Article.objects.get(id=id)

        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        article = self.get_object(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


######## Generic API Views ########


class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, # All these mixin functions have to be imported
                     mixins.CreateModelMixin, mixins.UpdateModelMixin, 
                     mixins.RetrieveModelMixin, mixins.DestroyModelMixin):

    serializer_class = ArticleSerializer # Specify our serializer
    queryset = Article.objects.all() # Specify out queryset
    lookup_field = 'id' # Lookupfield when we want to perform action on specific dataset

    # Commit 7 - Authentication
    # authentication_classes = [SessionAuthentication, BasicAuthentication] # Simple Authentication: Works with the Django Credentials
    authentication_classes = [TokenAuthentication] # Token Authentication: Has to be added in Admin Panel
    permission_classes = [IsAuthenticated] # Allows the user to retrieve the data only if authenticated

    def get(self, request, id=None): # GET or "if id:" --> retrieve detail from id
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request): # POST
        return self.create(request)

    def put(self, request, id): # PUT
        return self.update(request, id)

    def delete(self, request, id): # DELETE
        return self.destroy(request, id)


######## ViewSet API Views ########


class ArticleViewSet(viewsets.ViewSet): # I think Commit 8 - ViewSets don't bring any advantage...it's just more complicated with the router...

    def list(self, request): # GET All
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data) 

    def create(self, request): # POST
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None): # GET one - not working
        queryset = Article.objects.all()
        article = get_object_or_404(queryset, pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def update(self, request, pk=None): # PUT - not working
        article = Article.object.get(pk=pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None): # DELETE - not working
        article = Article.get_object(pk=pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)