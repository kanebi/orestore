from rest_framework import serializers 
from .models import Profile
from django.contrib.auth.models import User


# serializer for customer model
class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta :
        model = Profile
        fields = '__all__'
    def get_username(self, obj):
        return obj.user.username
class UserSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = '__all__'