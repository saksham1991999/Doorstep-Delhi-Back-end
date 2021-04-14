from django.forms import ModelForm

from versatileimagefield.fields import SizedImageCenterpointClickDjangoAdminField

from .models import ProductImage

class ProductImageForm(ModelForm):
    image = SizedImageCenterpointClickDjangoAdminField(required=False)

    class Meta:
        model = ProductImage
        fields = ('image','product', 'alt')
