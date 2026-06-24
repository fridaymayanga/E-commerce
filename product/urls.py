from django.urls import path
from product.views import ProductViews , SingleProductView,Saleview

urlpatterns =[
    path("sell/", SaleView.as_view()),
    path("",ProductViews.as_view()),
    path("<product_id>/", SingleProductView.as_view())
]