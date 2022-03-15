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


class SearchProductSerializer(serializers.Serializer):
    title = serializers.CharField(allow_null=True, max_length=255)
    variant = serializers.PrimaryKeyRelatedField(queryset=Variant.objects.all(), allow_null=True)
    price_start = serializers.FloatField(allow_null=True)
    price_end = serializers.FloatField(allow_null=True)
    created_date = serializers.DateField(allow_null=True)


class ProductVariantPricesSerializer(serializers.Serializer):
    price = serializers.FloatField()
    stock = serializers.FloatField()
    title = serializers.CharField(max_length=255)


class ProductImageSerializer(serializers.Serializer):
    product_image = serializers.ImageField()


class ProductCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    sku = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    product_image = serializers.ImageField()
    product_variant_prices = ProductVariantPricesSerializer(many=True)

    def validated_product_image(self, val):
        print("images are: ", val)
        return val

    def validate_product_variant_prices(self, val):
        print("price: ", val)
        return val
