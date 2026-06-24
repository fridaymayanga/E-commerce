from django.shortcuts import render, get_object_or_404
from rest_framework import views, generics, status,permissions
from rest_framework.response import Response 
from product.serializers import ProductSerializer, BulkProductionSerializer, SaleSerializer
from django.db import transaction
from product.models import ProductAlbum, Media, Product, Sale, ProductSale
from utils.pagination import CustomPagination
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q

# Create your views here.

class ProductViews(generics.GenericAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    def post(self,request):
        serializer = self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception = True)
        # price = serializer.validated_data.get("price")
        images = serializer.validated_data.pop("images",[])
        with transaction.atomic():
            album = ProductAlbum.objects.create()

            Media.objects.bulk_create(
                [Media(file=img, type = "IMAGE", album=album) for img in images]
            )
            serializer.save(seller = request.user, album=album)
            return Response(data=serializer.data, status=201)
    def get_queryset(self):
        search = self.request.query_params.get("search")
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        products = Product.objects.all().order_by("-created_at")
        if search:
            products = products.filter(Q(name__icontains=search) | Q(description__icontains=search))
        if min_price:
            min_price = float(min_price)
            products = products.filter(price__gte = min_price)
        if max_price:
            max_price = float(max_price)
            products = products.filter(price__Ite = max_price)
        return products
    @swagger_auto_schema(
        manual_parameters = [
            openapi.Parameter('search',openapi.IN_QUERY,
                description="search product by name",
                required = False, type=openapi.TYPE_STRING),
             openapi.Parameter('min_price',openapi.IN_QUERY,
                description="filter for lowest price",
                required=False, type= openapi.TYPE_NUMBER),
             openapi.Parameter('max_price', openapi.IN_QUERY,
             description='Filter for highest price',
             required=False, type = openapi.TYPE_NUMBER)

            ]
        )
    def get(self,request):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=200)


class SingleProductView(generics.GenericAPIView):
    permission_classes =[permissions.IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        product_id = self.kwargs["[product_id]"]
        product = get_object_or_404(prduct, id=product_id)
        return product

    def get (self,request,product_id):
        prduct = self,get_queryset()
        serializer = self.serializer_class(product)
        return Response (data=serializer.data, status=200)
    def patch(self,request,product_id):
        user = request.user
        product = self.get_queryset()
        if user != product.seller:
            return Response(data={"message":"Unathorised"},status=401)
        serializer = self.serializer_class(
            instance = product,
            data = request.data,
            partial = True
)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(data=serializer.data, status = 201)
    def delete(self, request, product_id):
        user = request.user
        product = self.get_queryset()
        if user != product.seller:
            return Response (data={"message":"Unauthorized"}, status=401)
        product.delete()
        return Response(status=204)
        
class SaleView(generics.GenericAPIView):
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        products = serializer.validated_data.pop("products")
        product_ids = [prod["id"] for prod in products]
        products_to_buy = Product.objects.filter(id__in = product_ids)
        total_amount = 0
        for buy_option in products:
            id = buy_option["id"]
            quantity = buy_option["quantity"]
            prd = products_to_buy.filter(id = id).first()
            if not prd:
                return Response(data={"message": f"Product with id {id} not found"}, status=400)
            if prd.quantity < quantity:
                return Response(data={"message": "quantity is more than what is available"}, status=400)
            total_amount += quantity * prd.price
        sale = Sale.objects.create(buyer=request.user, total_amount=total_amount)
        for buy_option in products:
            id = buy_option["id"]
            quantity = buy_option["quantity"]
            prd = products_to_buy.filter(id = id).first()
            ProductSale.objects.create(
                product = prd,
                sale = sale,
                quantity = quantity,
                price = prd.price
            )
            prd.quantity -= quantity
            prd.quantity_sold += quantity
            prd.save()
        return Response(data={"message": "Success!"}, status=200)        