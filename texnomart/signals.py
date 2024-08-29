import os
import json
import logging

from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from pathlib import Path
from root import settings
from root.settings import BASE_DIR
from texnomart.models import CategoryModel, ProductModel

logger = logging.getLogger(__name__)

# Category send email


def send_category_email(subject, message):
    email_from = settings.DEFAULT_FROM_EMAIL
    email_to = [settings.TEACHER_EMAIL]
    try:
        send_mail(subject, message, email_from, email_to)
        logger.info(f'Email sent to {settings.TEACHER_EMAIL}')
    except Exception as Exc:
        raise logger.error(f'Error sending email: {str(Exc)}')


@receiver(post_save, sender=CategoryModel)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        subject = 'New Category is CREATED!'
        message = f'New Category name: "{instance.title}"'
    else:
        subject = 'Category is EDITED!'
        message = f'The "{instance.title}" Category has been EDITED!'

    send_category_email(subject, message)


@receiver(pre_delete, sender=CategoryModel)
def category_delete(sender, instance, **kwargs):
    directory = 'deleted_categories/'
    directory_path = Path(settings.BASE_DIR) / directory
    directory_path.mkdir(parents=True, exist_ok=True)
    file_path = directory_path / f'{instance.title}-category.json'
    category_data = {
        'id': instance.id,
        'title': instance.title,
    }
    try:
        with open(file_path, mode='w') as file_json:
            json.dump(category_data, file_json, indent=4)
        print(f'{instance.title} is deleted and data saved to {file_path}')
    except IOError as e:
        print(f'Error writing file {file_path}: {str(e)}')


# Product send email


def send_product_email(subject, message):
    email_from = settings.DEFAULT_FROM_EMAIL
    email_to = [settings.TEACHER_EMAIL]
    try:
        send_mail(subject, message, email_from, email_to)
        logger.info(f'Email sent to {settings.TEACHER_EMAIL}')
    except Exception as Exc:
        raise logger.error(f'Error sending email: {str(Exc)}')


@receiver(post_save, sender=ProductModel)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        subject = 'New Product is CREATED!'
        message = f'New Product name: "{instance.name}"'
    else:
        subject = 'Product is EDITED!'
        message = f'The "{instance.name}" Product has been EDITED!'

    send_product_email(subject, message)


@receiver(pre_delete, sender=ProductModel)
def product_delete(sender, instance, **kwargs):
    directory = 'deleted_products/'
    directory_path = Path(settings.BASE_DIR) / directory
    directory_path.mkdir(parents=True, exist_ok=True)
    file_path = directory_path / f'{instance.name}-product.json'
    product_data = {
        'id': instance.id,
        'name': instance.name,
    }
    try:
        with open(file_path, mode='w') as file_json:
            json.dump(product_data, file_json, indent=4)
        print(f'{instance.name} is deleted and data saved to {file_path}')
    except IOError as e:
        print(f'Error writing file {file_path}: {str(e)}')
