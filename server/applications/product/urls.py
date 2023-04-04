from applications.product.views import ListProductDetail
from django.urls import include, path

urlpatterns = [
    path('lpd', ListProductDetail.as_view(), name='lpd'),
]