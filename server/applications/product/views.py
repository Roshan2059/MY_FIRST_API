from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class ListProductDetail(APIView):
    def get(self, request,format=None):
        pro = Product.objects.all()
        serializer=ProductSerializer(pro, many=True)
        return Response(serializer.data)
    
    def post(self, request,format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data created'}, status=201)
        return Response(serializer.errors,status=404)
