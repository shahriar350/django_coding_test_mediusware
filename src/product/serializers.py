from rest_framework import serializers

from product.models import Product, ProductVariantPrice, ProductVariant, Variant


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = (
            'id',
            'title',
            'description',
            'active',
        )


class ProductVariantSerializer(serializers.ModelSerializer):
    variant = VariantSerializer()

    class Meta:
        model = ProductVariant
        fields = (
            'id',
            'variant_title',
            'variant',
            'product',
        )


class ProductVariationPriceSerializer(serializers.ModelSerializer):
    product_variant_one = ProductVariantSerializer()
    product_variant_two = ProductVariantSerializer()
    product_variant_three = ProductVariantSerializer()

    class Meta:
        model = ProductVariantPrice
        fields = (
            'id',
            'product_variant_one',
            'product_variant_two',
            'product_variant_three',
            'price',
            'stock',
            'product',
        )


class ProductSerializer(serializers.ModelSerializer):
    get_product_variation_prices = ProductVariationPriceSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'sku',
            'description',
            'created_at',
            'updated_at',
            'get_product_variation_prices',
        )
