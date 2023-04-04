from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/account/', include('applications.account.urls'),),
    path('', include('applications.product.urls'),),


] + static(settings.MEDIA_URL,
           document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
