# To be used in "python manage.py shell"
# Example of how to convert from Database Entry to Serialized Data (Dictionary) and then to JSON Data

from api_basic.models import Article
from api_basic.serializers import ArticleSerializer

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


a = Article(title='NewTitle', author='NewName', email='test@test.de') # Add Entry in Database
a.save()

serializer = ArticleSerializer(a) # Serialize Article a
print(serializer.data)

content = JSONRenderer().render(serializer.data) # JSON Article a
print(content)

serializer = ArticleSerializer(Article.objects.all(), many = True) # Serialize all Articles
print(serializer.data)

content = JSONRenderer().render(serializer.data) # JSON all Articles
print(content)