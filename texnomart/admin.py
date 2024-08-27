from django.contrib import admin
#from rest_framework.authtoken.models import Token

from texnomart.models import CategoryModel, ProductModel, CommentModel, ImageModel, AttributeModel, KeyModel, ValueModel


# @admin.register(CategoryModel)
# class CategoryAdmin(admin.ModelAdmin):
#     exclude = ('slug',)
#     list_display = ('title', 'slug')
#     search_fields = ('title', 'slug')
#     list_filter = ('title', 'created_at')


admin.site.register(CategoryModel)
admin.site.register(ProductModel)
admin.site.register(CommentModel)
admin.site.register(ImageModel)
admin.site.register(KeyModel)
admin.site.register(ValueModel)
admin.site.register(AttributeModel)
