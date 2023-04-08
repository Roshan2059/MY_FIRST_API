from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

class ListProductView(APIView):
    def get(self, request,format=None):
        pro = Product.objects.filter(is_active=True)
        serializer=ProductSerializer(pro, many=True)
        return Response(serializer.data)
    
    def post(self, request,format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class UpdateDeleteView(APIView):
    def get_object(self, id):
        try:
            return Product.objects.get(id=id, is_active=True)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def get(self, request, id,format=None):
        pro = self.get_object(id)
        serializer=ProductSerializer(pro)
        return Response(serializer.data)

    def put(self, request, id):
        pro = self.get_object(id)
        serializer = ProductSerializer(pro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        product = self.get_object(id)
        product.is_active = False
        product.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # def put(self, request, pk, format=None):
    #     product = self.get_object(pk)
    #     serializer = ProductSerializer(product, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, format=None):
    #     product = self.get_object(pk)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    
    # def make_isActive_false(self, request, pk):
    #     product = self.get_object(pk)
    #     serializer = ProductSerializer(product, data=request.data)
    #     if serializer.is_active == True:
    #         serializer.is_active == False
    #     else:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
