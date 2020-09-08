from django.contrib import admin
from .models import MobileShop, PickUP, SmsOTP, OfferImages
# Register your models here.
class RatingAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)

admin.site.register(MobileShop)
admin.site.register(PickUP)
admin.site.register(SmsOTP, RatingAdmin)
admin.site.register(OfferImages)