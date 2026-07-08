from rest_framework import serializers
from .models import Category, Cast, Movie, Series


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cast
        fields = ['id', 'name']


class MovieSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    casts = serializers.PrimaryKeyRelatedField(queryset=Cast.objects.all(), many=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_date', 'categories', 'casts', 'poster_image']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['categories'] = [str(category) for category in instance.categories.all()]
        representation['casts'] = [str(cast) for cast in instance.casts.all()]
        return representation


class SeriesSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    casts = serializers.PrimaryKeyRelatedField(queryset=Cast.objects.all(), many=True)

    class Meta:
        model = Series
        fields = ['id', 'title', 'description', 'release_date', 'categories', 'casts', 'poster_image']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['categories'] = [str(category) for category in instance.categories.all()]
        representation['casts'] = [str(cast) for cast in instance.casts.all()]
        return representation
