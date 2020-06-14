# To be used in "python manage.py shell"
# Proves that the ModelSerializer works as well as the Standard Serializer but is a lot shorter

from api_basic.models import Article
from api_basic.serializers import ArticleSerializer

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


serializer = ArticleSerializer()

print(repr(serializer))