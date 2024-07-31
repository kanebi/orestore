from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.views import APIView, Response, status
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from .serializers import UserProfileSerializer,UserSerializer
from .models import Profile

class RegisteredUsers(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser] #makes this only viewable to staffs/admins
    
    
class UserProfile(ViewSet):
    permission_classes =[IsAuthenticated]
    @action(['GET'], detail=True)
    def get_my_profile(self, request):
        # get customer profile or create new if it does not exist in the system
        user_profile = Profile.objects.get(user = request.user)
        #serialize the profile to json format for response
        serialized_profile = UserProfileSerializer(user_profile)
        return Response (serialized_profile.data, status=status.HTTP_200_OK)

    
    