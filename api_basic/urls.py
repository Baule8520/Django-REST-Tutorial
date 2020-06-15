from django.urls import path, include
from .views import article_list, article_detail, ArticleAPIView, ArticleAPIDetail, GenericAPIView, ArticleViewSet
from rest_framework.routers import DefaultRouter # Import Router for ViewSet

router = DefaultRouter() # Registering Router for ViewSet
router.register('article', ArticleViewSet, basename='article')

# The API Url's (to test you can use Postman)

urlpatterns = [
    path('article/', article_list), # GET: Gives a list of all articles, POST: Creates a new entry
    path('detail/<int:pk>/', article_detail), # GET, PUT (Update information), DELETE single Articles indentified by integer "pk" (primary Key)

    path('API/', ArticleAPIView.as_view()), # Commit 5 - Use Class Based Views - GET: Gives a list of all articles, POST: Creates a new entry
    path('APIDetail/<int:id>/', ArticleAPIDetail.as_view()), # Commit 5 - Use Class Based Views - GET, PUT (Update information), DELETE single Articles indentified by integer "id"

    path('GenericAPI/', GenericAPIView.as_view()), # Commit 6 - Generic API Views - GET, POST
    path('GenericAPI/<int:id>/', GenericAPIView.as_view()), # Commit 6 - Generic API Views - GET, PUT, DELETE

    path('viewset/', include(router.urls)), # Commit 8 & 9 - ViewSet - GET, POST
    path('viewset/<int:pk>', include(router.urls)), # Commit 9 - Generic ViewSet GET, PUT, DELETE
]