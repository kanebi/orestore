from django.urls import path, include
from .api import UserProfile, RegisteredUsers
from rest_framework import routers
from .views import index,user_profile

router = routers.DefaultRouter()
router.register(r'users',RegisteredUsers, 'registered-users' )

urlpatterns = [
    path("",index, name='home'),

    path(r"", include('restaurant.urls')),
    path("", include(router.urls)),
    path(r"profile", UserProfile.as_view({'get':'get_my_profile'})),

    path("accounts/profile/",user_profile, name='profile'),

    
]

