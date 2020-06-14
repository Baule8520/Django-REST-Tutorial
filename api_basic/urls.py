from django.urls import path
from .views import article_list, article_detail, ArticleAPIView, ArticleAPIDetail

# The API Url's (to test you can use Postman)

urlpatterns = [
    path('article/', article_list), # GET: Gives a list of all articles, POST: Creates a new entry
    path('detail/<int:pk>/', article_detail), # GET, PUT (Update information), DELETE single Articles indentified by integer "pk" (primary Key)

    path('API/', ArticleAPIView.as_view()), # Commit 5 - Use Class Based Views - GET: Gives a list of all articles, POST: Creates a new entry
    path('APIDetail/<int:id>/', ArticleAPIDetail.as_view()), # Commit 5 - Use Class Based Views - GET, PUT (Update information), DELETE single Articles indentified by integer "id"
]