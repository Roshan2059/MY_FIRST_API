
from applications.account.views import AddProfileImageAPIView, DeleteUserAPIView, \
    ForgotAPIView,  GetAllUsersAPIView,  RegisterAPIView, ResetAPIView, \
    UserAPIView
from django.urls import include, path

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='register'),
    path('forgot', ForgotAPIView.as_view(), name='forgot'),
    path('password_reset/', include('django_rest_passwordreset.urls',
         namespace='password_reset')),
    path('user', UserAPIView.as_view(), name='user'),
    path('user/all', GetAllUsersAPIView.as_view(), name='all_user'),
    path('user/delete/<pk>', DeleteUserAPIView.as_view(), name='all_user'),
    path('user/update-profile-image/<pk>', AddProfileImageAPIView.as_view(),
         name='update_profile_image'),

]
