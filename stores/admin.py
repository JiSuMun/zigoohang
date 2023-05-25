from django.contrib import admin
from .models import *


admin.site.register(Store)
admin.site.register(Product)
admin.site.register(ProductReview)

# admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)