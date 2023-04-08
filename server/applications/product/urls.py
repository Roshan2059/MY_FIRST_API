from applications.product.views import ListProductView,UpdateDeleteView
from django.urls import include, path

urlpatterns = [
    path('lpd', ListProductView.as_view(), name='lpd'),
    # path('update', )
    path('uod/<int:id>', UpdateDeleteView.as_view(), name='uod')
]