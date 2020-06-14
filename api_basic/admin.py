from django.contrib import admin

from .models import Article

# Register your models here.

admin.site.register(Article)    # Class Article can now be shown and modified in Admin Dashboard