from django.views import generic
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from config.mixins import PostPagination
from product.models import Variant, Product
from product.serializers import ProductSerializer


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


class APIProductList(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = PostPagination

    def get_queryset(self):
        return Product.objects.prefetch_related('get_product_variation_prices__product_variant_one__variant',
                                                'get_product_variation_prices__product_variant_two__variant',
                                                'get_product_variation_prices__product_variant_three__variant')
