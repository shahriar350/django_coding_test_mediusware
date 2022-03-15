import json

import ujson

import django_filters
from django.db import transaction
from django.db.models import Q
from django.views import generic
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from config.mixins import PostPagination
from product.models import Variant, Product, ProductVariant, ProductVariantPrice, ProductImage
from product.serializers import ProductSerializer, VariantSerializer, SearchProductSerializer, ProductCreateSerializer


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


class APIVariantList(ListAPIView):
    serializer_class = VariantSerializer
    queryset = Variant.objects.all()


class APIProductSearch(ListAPIView):
    serializer_class = ProductSerializer

    pagination_class = PostPagination

    def get_queryset(self):
        title = self.request.query_params.get('title', None)
        variant = self.request.query_params.get('variant', None)
        price_start = self.request.query_params.get('price_start', None)
        price_end = self.request.query_params.get('price_end', None)
        created_date = self.request.query_params.get('created_date', None)

        products = Product.objects.all()

        if variant:
            products = products.filter(get_product_variant__variant_id=variant)
        if price_start and price_end:
            products = products.filter(get_product_variation_prices__price__range=(price_start, price_end))
        if title:
            products = products.filter(title__icontains=title)
        if created_date:
            products = products.filter(created_at__date=created_date)

        return products.distinct()
    # Product.objects.filter(title__icontains=title)


class APIProductCreate(APIView):
    # parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, format=None):
        title = request.data.get('title')
        sku = request.data.get('sku')
        description = request.data.get('description')
        # print(type(request.data.get('product_variant_prices')))

        product_variant_prices = json.loads(request.data.getlist('product_variant_prices')[0])
        product_variants = json.loads(request.data.getlist('product_variant')[0])
        product_images = []
        for i in request.FILES.getlist('product_image'):
            product_images.append(i)
        with transaction.atomic():
            product = Product.objects.create(title=title, sku=sku, description=description)
            product_variant_one = None
            product_variant_two = None
            product_variant_three = None
            for data in product_variant_prices:
                title_split = data['title'].split("/")
                title_split.pop()
                # print("split: ", title_split)
                # [{asfd/erg/}]
                for index, val in enumerate(title_split):  # asfd
                    for variance in product_variants:
                        for item in variance['tags']:
                            if val == item:
                                dataVariation = ProductVariant.objects.create(variant_title=title_split[index],
                                                                              variant_id=variance['option'],
                                                                              product=product)

                                if data and index == 0:
                                    product_variant_one = dataVariation

                                elif data and index == 1:
                                    product_variant_two = dataVariation

                                elif data and index == 3:
                                    product_variant_three = dataVariation

                variation = ProductVariantPrice(price=data['price'],
                                                stock=data['stock'], product=product)

                if product_variant_one is not None:
                    variation.product_variant_one = product_variant_one
                if product_variant_two is not None:
                    variation.product_variant_two = product_variant_two
                if product_variant_three is not None:
                    variation.product_variant_three = product_variant_three
                variation.save()
            print(product_images)
            for i in product_images:
                productimage = ProductImage.objects.create(product=product, file_path=i)
                print(productimage)

            return Response(status=status.HTTP_200_OK)
            # raise ValueError("error")
