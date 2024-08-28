# from django.contrib.auth.models import User
# from django.db.models.signals import post_save, pre_save, post_delete
# from django.dispatch import receiver
# from django.middleware import cache
# from rest_framework.authtoken.models import Token
# from texnomart.models import ProductModel
#
#
# @receiver(post_save, sender=User)
# def save_profile(sender, instance, created, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
#
#
# @receiver(post_delete, sender=ProductModel)
# @receiver(pre_save, sender=ProductModel)
# @receiver(post_save, sender=ProductModel)
# def saved_product(sender, instance, **kwargs):
#     category_slug = kwargs.get('slug')
#     cache.delete(f'product_list_{category_slug}')
#     cache.delete(f'product_detail_{instance.slug}')
