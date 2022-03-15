from django.urls import path
from django.views.generic import TemplateView

from product.views.product import CreateProductView,APIRemoveVariation, APIAddVariation,APIProductList, APIVariantList,APIProductSearch,APIProductCreate,APIEditProduct,EditTemplate,APIBasicUpdate,APIAddImage
from product.views.variant import VariantView, VariantCreateView, VariantEditView

app_name = "product"

urlpatterns = [
    # Variants URLs
    path('variants/', VariantView.as_view(), name='variants'),
    path('variant/create', VariantCreateView.as_view(), name='create.variant'),
    path('variant/<int:id>/edit', VariantEditView.as_view(), name='update.variant'),

    # Products URLs
    path('create/', CreateProductView.as_view(), name='create.product'),
    path('list/', TemplateView.as_view(template_name='products/list.html', extra_context={
        'product': True
    }), name='list.product'),
    path('edit/<int:pk>/', EditTemplate.as_view(),name="edit.product"),

    path('api/list/', APIProductList.as_view()),
    path('api/variant/list/', APIVariantList.as_view()),
    path('api/product/search/', APIProductSearch.as_view()),
    path('api/product/create/', APIProductCreate.as_view()),
    path('api/product/edit/<int:pk>/', APIEditProduct.as_view()),
    path('api/product/update/basic/<int:pk>/', APIBasicUpdate.as_view()),
    path('api/add/image/<int:pk>/', APIAddImage.as_view()),
    path('api/add/variation/<int:pk>/', APIAddVariation.as_view()),
    path('api/remove/variation/<int:pk>/', APIRemoveVariation.as_view()),
]
