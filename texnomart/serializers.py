from django.db.models import Avg
from django.db.models.functions import Round
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from texnomart.models import CategoryModel, ProductModel, CommentModel, AttributeModel, KeyModel, ValueModel


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    def get_product_count(self, obj):
        return obj.product_count

    class Meta:
        model = CategoryModel
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_is_liked(self, product):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return product.is_liked.filter(id=request.user.id).exists()
        return False

    def get_image(self, products):
        request = self.context.get('request')
        try:
            image = products.images.get(is_primary=True)
            return request.build_absolute_uri(image.image.url)
        except products.images.model.DoesNotExist:
            return None

    class Meta:
        model = ProductModel
        fields = '__all__'


class ProductModelSerializer(ModelSerializer):
    category = serializers.CharField(source="category.title")
    is_liked_count = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField(method_name='get_image')
    avg_rating = serializers.SerializerMethodField(method_name='get_avg_rating')
    all_images = serializers.SerializerMethodField(method_name='get_all_images')
    attributes = serializers.SerializerMethodField(method_name='get_attribute')

    def get_is_liked_count(self, obj):
        return obj.is_liked.count()

    def get_attribute(self, instance):
        attributes = [{str(attribute.key): str(attribute.value)} for attribute in instance.attributes.all()]
        return attributes

    def get_comment_info(self, obj):
        comment_count = obj.comments.count()
        comments = obj.comments.all().values('comment', 'rating', 'user__username')
        return {
            'comment_count': comment_count,
            'comments': list(comments)
        }

    def get_all_images(self, instance):
        request = self.context.get('request')
        images = instance.images.all().order_by('-is_primary', '-id')
        all_image = []
        for image in images:
            all_image.append(request.build_absolute_uri(image.image.url))
        return all_image

    def get_avg_rating(self, obj):
        avg_rating = obj.comments.all().aggregate(avg_rating=Round(Avg('rating')))
        return avg_rating

    def get_image(self, obj):
        image = obj.images.filter(is_primary=True).first()
        if image:
            image_url = image.image.url
            request = self.context.get('request')
            return request.build_absolute_uri(image_url)


    class Meta:
        model = ProductModel
        fields = '__all__'


class AttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttributeModel
        fields = '__all__'


class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyModel
        fields = '__all__'


class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValueModel
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, required=True)

    class Meta:
        fields = ['username', 'password']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data


    def create(self, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


