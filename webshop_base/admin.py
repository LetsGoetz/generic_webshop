from typing import Set

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# webshop_base models ----start
from .models import Customer
from .models import CustomerNewPostData
from .models import CustomerPhone
from .models import PstalAddress
from .models import CustomerCategory
from .models import ProductItem
from .models import ProductPrice
from .models import ProductCategory
from .models import ProductOrder
from .models import Order
from .models import ProductImage
from .models import OrderStatus
from .models import DeliveryOption
from .models import Rebate
from .models import RebateAction
from .models import MailingAction
from .models import MailMessage
from .models import UserCorrespondence
from .models import TypeOfCorrespondence
from .models import LinkFollowup
from .models import PromoCodeAction
from .models import ProductReview
from .models import ProductReturn
from .models import ReturnStatus
# webshop_base models ----end

##inline_definions -----------------------START

class CustomerInline(admin.TabularInline):
    model = Customer
class CustomerNewPostDataInline(admin.TabularInline):
    model = CustomerNewPostData
class CustomerPhoneInline(admin.TabularInline):
    model = CustomerPhone
class PstalAddressInline(admin.TabularInline):
    model = PstalAddress
class ProductPriceInline(admin.TabularInline):
    model = ProductPrice
class ProductOrderInline(admin.TabularInline):
    model = ProductOrder
class OrderInline(admin.TabularInline):
    model = Order
class ProductImageInline(admin.TabularInline):
    model = ProductImage
class RebateInline(admin.TabularInline):
    model = Rebate
class RebateActionInline(admin.TabularInline):
    model = RebateAction
class MailingActionInline(admin.TabularInline):
    model = MailingAction
class UserCorrespondenceToCustomerInline(admin.TabularInline):
    model = UserCorrespondence
    fk_name = "ref_user"
class UserCorrespondenceToMailInline(admin.TabularInline):
    model = UserCorrespondence
    fk_name = "ref_message"
class UserCorrespondencetoTypeInline(admin.TabularInline):
    model = UserCorrespondence
    fk_name = "ref_type_of_message"
class PromoCodeActionInline(admin.TabularInline):
    model = PromoCodeAction
class ProductReviewInline(admin.TabularInline):
    model = ProductReview
class ProductReturnInline(admin.TabularInline):
    model = ProductReturn
##inline_definions -----------------------END


# Unregister the provided model admin
admin.site.unregister(User)

# Register out own model admin, based on the default UserAdmin
@admin.register(User)
class CustomUserAdmin(UserAdmin):

    actions = [
        'activate_users',
    ]

    inlines = [
        UserCorrespondenceToCustomerInline
    ]

    def activate_users(self, request, queryset):
        assert request.user.has_perm('auth.change_user')
        cnt = queryset.filter(is_active=False).update(is_active=True)
        self.message_user(request, 'Activated {} users.'.format(cnt))
    activate_users.short_description = 'Activate Users'  # type: ignore

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('auth.change_user'):
            del actions['activate_users']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()  # type: Set[str]

        if not is_superuser:
            disabled_fields |= {
                'username',
                'is_superuser',
                'user_permissions',
            }

        # Prevent non-superusers from editing their own permissions
        if (
            not is_superuser
            and obj is not None
            and obj == request.user
        ):
            disabled_fields |= {
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form
class CustomUserAdminInline(admin.TabularInline):
    model = User

class CustomerAdmin(admin.ModelAdmin):
    inlines = [
        CustomerNewPostDataInline,
        CustomerPhoneInline,
        PstalAddressInline,
        OrderInline,
        ProductReviewInline,
    ]
admin.site.register(Customer, CustomerAdmin)


class CustomerNewPostDataAdmin(admin.ModelAdmin):
    inlines = [
        
    ]

admin.site.register(CustomerNewPostData,CustomerNewPostDataAdmin)


class CustomerPhoneAdmin(admin.ModelAdmin):
    inlines = [
        
    ]
admin.site.register(CustomerPhone,CustomerPhoneAdmin)


class PstalAddressAdmin(admin.ModelAdmin):
    inlines = [
        
    ]
admin.site.register(PstalAddress,PstalAddressAdmin)


class CustomerCategoryAdmin(admin.ModelAdmin):
    inlines = [
        MailingActionInline
    ]
admin.site.register(CustomerCategory,CustomerCategoryAdmin)


class ProductItemAdmin(admin.ModelAdmin):
    inlines = [
        ProductPriceInline,
        ProductOrderInline,
        ProductImageInline,
        RebateInline,
        ProductReviewInline
    ]
admin.site.register(ProductItem,ProductItemAdmin)


class ProductPriceAdmin(admin.ModelAdmin):
    inlines = [
        
    ]
admin.site.register(ProductPrice,ProductPriceAdmin)


class ProductCategoryAdmin(admin.ModelAdmin):
    inlines = [
        
    ]
admin.site.register(ProductCategory,ProductCategoryAdmin)


class ProductOrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductReturnInline
    ]
admin.site.register(ProductOrder,ProductOrderAdmin)


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductOrderInline,
    ]
admin.site.register(Order,OrderAdmin)


class ProductImageAdmin(admin.ModelAdmin):
    inlines = [
        
    ]
admin.site.register(ProductImage,ProductImageAdmin)


class OrderStatusAdmin(admin.ModelAdmin):
    inlines = [
        OrderInline
    ]
admin.site.register(OrderStatus,OrderStatusAdmin)


class DeliveryOptionAdmin(admin.ModelAdmin):
    inlines = [
        OrderInline
    ]
admin.site.register(DeliveryOption,DeliveryOptionAdmin)


class RebateAdmin(admin.ModelAdmin):
    inlines = [
        
    ]
admin.site.register(Rebate,RebateAdmin)


class RebateActionAdmin(admin.ModelAdmin):
    inlines = [
        MailingActionInline,
        PromoCodeActionInline,
    ]
admin.site.register(RebateAction,RebateActionAdmin)


class MailingActionAdmin(admin.ModelAdmin):
    inlines = [
        
    ]
admin.site.register(MailingAction,MailingActionAdmin)


class MailMessageAdmin(admin.ModelAdmin):
    inlines = [
        MailingActionInline,
        UserCorrespondenceToMailInline,
    ]
admin.site.register(MailMessage,MailMessageAdmin)


class UserCorrespondenceAdmin(admin.ModelAdmin):
    inlines = [
        
    ]
admin.site.register(UserCorrespondence,UserCorrespondenceAdmin)


class TypeOfCorrespondenceAdmin(admin.ModelAdmin):
    inlines = [
        UserCorrespondencetoTypeInline
    ]
admin.site.register(TypeOfCorrespondence, TypeOfCorrespondenceAdmin)


class LinkFollowupAdmin(admin.ModelAdmin):
    inlines = [
        OrderInline,
    ]
admin.site.register(LinkFollowup,LinkFollowupAdmin)


class PromoCodeActionAdmin(admin.ModelAdmin):
    inlines = [
        OrderInline
    ]
admin.site.register(PromoCodeAction,PromoCodeActionAdmin)


class ProductReviewAdmin(admin.ModelAdmin):
    inlines = [
        
    ]
admin.site.register(ProductReview,ProductReviewAdmin)


class ProductReturnAdmin(admin.ModelAdmin):
    inlines = [
        
    ]
admin.site.register(ProductReturn,ProductReturnAdmin)


class ReturnStatusAdmin(admin.ModelAdmin):
    inlines = [
        ProductReturnInline
    ]
admin.site.register(ReturnStatus,ReturnStatusAdmin)

