from rest_framework import serializers  # REST Framework import Serializer for JSON Conversion and Unconversion

from .models import Article     # Import the Database class


#class ArticleSerializer(serializers.Serializer): # Commit 1 - Standard Serializer, all Form Objects have to be entered manually
 #   title = serializers.CharField(max_length=100)
  #  author = serializers.CharField(max_length=100)
   # email = serializers.EmailField(max_length=100)
    #date = serializers.DateTimeField()

    
#    def create(self, validated_data): # Create Database entry
 #       
  #      return Article.objects.create(validated_data)

    
#    def update(self, instance, validated_data): # Update Database entry
 #       instance.title = validated_data.get('title', instance.title)
  #      instance.author = validated_data.get('author', instance.author)
   #     instance.email = validated_data.get('email', instance.email)
    #    instance.date = validated_data.get('date', instance.date)
     #   
      #  instance.save()

        #return instance


class ArticleSerializer(serializers.ModelSerializer): # Commit 2 - the lot easier ModelSerializer
    class Meta:
        model = Article
        fields = '__all__' # When you want to display the whole model in JSON Response
        # fields = ['title', 'author'] <-- When you want to specify what data will be transfered
