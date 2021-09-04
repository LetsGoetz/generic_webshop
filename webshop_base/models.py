from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from django.contrib.auth.models import User

## bases ----------------------------------------------
class AbstractBase(models.Model):
    name =  models.CharField(max_length=200, null=True)
    description =  models.CharField(max_length=200, null=True)
    modification_date =  models.DateTimeField(auto_now=True, null=True)
    modification_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="+", null = True)
    creation_date =  models.DateTimeField(auto_now_add=True, null=True)
    creation_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="+", null=True)


    class Meta:
        abstract = True


class AbstractStatusBase(AbstractBase):
	send_mail_on_init = models.BooleanField(default=False) # should customer be informed vie email when this status is initiated?
	bg_color =  models.CharField(max_length=50, null=True)

	class Meta:
		abstract = True


## customer data ------------------------------------

class Customer(AbstractBase):
	# userFields: https://docs.djangoproject.com/en/3.2/ref/contrib/auth/#django.contrib.auth.models.User
	ref_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
	ref_category =  models.ManyToManyField('CustomerCategory')
	customer_birthday =  models.DateField(null=True)
	fathers_name =  models.CharField(max_length=200, null=True)
	is_newsLetter_required =  models.BooleanField(default=False)
	# language:  TODO # Later for Multilang # maybe # one day # let's see
	
	def user_images_path(instance, filename):
		# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
		return 'user_{0}/{1}'.format(instance.ref_user.id, filename)
	
	avatar_image =  models.ImageField(null=True, upload_to=user_images_path)

	def clean(self):
		super().clean()
		if self.ref_user is None:
			raise ValidationError('A User must be assigned to the Customer instance')

	def __str__(self):
		return self.name

# Spezifische Klasse
class CustomerNewPostData(AbstractBase):
	ref_customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True)
	new_post_number =  models.CharField(max_length=100, null=True)
	new_post_address =  models.CharField(max_length=200, null=True)

	class Meta():
		verbose_name_plural = "CustomerNewPostData"

	def clean(self):
		super().clean()
		if self.ref_customer is None:
			raise ValidationError('A Customer must be assigned to this instance')

	def __str__(self):
		return self.newPostNumber


class CustomerPhone(AbstractBase):
	ref_customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True)
	phone_number = models.CharField(max_length=50, null=True)

	def clean(self):
		super().clean()
		if self.ref_customer is None:
			raise ValidationError('A Customer must be assigned to this instance')


	def __str__(self):
		return self.phone_number


class PstalAddress(AbstractBase):
	# Teilweise spezifische Attribute
	#https://pypi.org/project/django-countries/
	country =  CountryField(blank_label='(select country)', null=True,)
	oblast =   models.CharField(max_length=100, null=True)
	city =   models.CharField(max_length=100, null=True,)
	raion =   models.CharField(max_length=100, null=True,)
	settlement =   models.CharField(max_length=100, null=True)
	postalCode =   models.CharField(max_length=100, null=True)
	StreetNumber =  models.CharField(max_length=200, null=True)
	staircase =  models.CharField(max_length=100, null=True)
	flat =  models.CharField(max_length=50, null=True)
	ref_customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True)

	class Meta():
		verbose_name_plural = "PstalAddresses"

	def clean(self):
		super().clean()
		if self.ref_customer is None:
			raise ValidationError('A Customer must be assigned to this instance')

	def __str__(self):
		return self.postalCode + ', ' + self.settlement + ', ' + self.StreetNumber


class CustomerCategory(AbstractBase):
	products_visible_for_this_category = models.ManyToManyField('ProductItem')

	class Meta():
		verbose_name_plural = "CustomerCategories"

	
	def clean(self):
		super().clean()
		if self.name is None:
			raise ValidationError('At least a name must be assigned to this instance')

	def __str__(self):
		return self.name

## products and orders ---------------------------------------------------

class ProductItem(AbstractBase):
	measurement_unit_name_single =  models.CharField(max_length=200, null=True) # kg/liter/piece...
	measurement_unit_name_plural =  models.CharField(max_length=200, null=True) # kgs/liters/pieces...
	quantity_in_stock =  models.IntegerField(default=0) # of measurementUnits
	selling_unit = models.DecimalField(max_digits=3, decimal_places=2, default=0.00) # number of measurementUnit's

	def clean(self):
		super().clean()
		if self.name is None or self.measurement_unit_name_single is None:
			raise ValidationError('At least a product name and a measurement unit name must be specified')

	def __str__(self):
		return self.name


class ProductPrice (AbstractBase):
	ref_product = models.ForeignKey('ProductItem', on_delete=models.PROTECT, null=True)
	currency = models.CharField(max_length=50, null=True)
	quantity_SU_from  =  models.IntegerField(null=True) # of selling units
	quantity_SU_to = models.IntegerField(null=True) # of sellingunits
	ref_customer_group = models.ManyToManyField('CustomerCategory') # for which customer category to implement
	price_for_one_SU = models.DecimalField(max_digits=10, decimal_places=2, null=True)

	def clean(self):
		super().clean()
		if self.ref_product is None or self.price_for_one_SU is None:
			raise ValidationError('At least a product and a price of a selling unit must be specified')


class ProductCategory(AbstractBase):
	
	category_products = models.ManyToManyField('ProductItem')

	class Meta():
		verbose_name_plural = "ProductCategories"
	
	def product_category_path(instance, filename):
		# file will be uploaded to MEDIA_ROOT/product_category_<id>/<filename>
		return 'product_category_{0}/{1}'.format(instance.id, filename)
	category_image =  models.ImageField(upload_to=product_category_path, null=True)

	def clean(self):
		super().clean()
		if self.name is None:
			raise ValidationError('At least a name must be specified')


	def __str__(self):
		return self.name
	

class ProductOrder(AbstractBase):
	ref_product = models.ForeignKey('ProductItem', on_delete=models.PROTECT, null=True)
	ref_order = models.ForeignKey('Order', on_delete=models.PROTECT, null=True)
	quantity_of_SU =  models.IntegerField(null=True) # SU == Selling unit
	ref_price = models.ForeignKey('ProductPrice', on_delete=models.PROTECT, null=True)

	def clean(self):
		super().clean()
		if self.ref_product is None or self.ref_price is None or self.quantity_of_SU is None:
			raise ValidationError('Product, Price and quantity of Selling Units must be specified')


class Order(AbstractBase):
	ref_customer = models.ForeignKey('Customer', on_delete=models.PROTECT, null=True)
	ref_delivery = models.ForeignKey('DeliveryOption', on_delete=models.PROTECT, null=True)
	order_date =  models.DateTimeField(auto_now_add=True, null=True)
	delivery_date =  models.DateField(null=True)
	customer_note =  models.TextField(null=True)
	ref_order_status = models.ForeignKey('OrderStatus', on_delete=models.PROTECT, null=True)
	 # wenn ein order während einer mailing action followup session platziert wurde - für Analyse, erkennst am url token
	ref_link_followup = models.ForeignKey('LinkFollowup', on_delete=models.SET_NULL, null=True)
	# das gleiche für promocodes
	ref_promocode_followup = models.ForeignKey('PromoCodeAction', on_delete=models.SET_NULL, null=True)

	def clean(self):
		super().clean()
		if self.ref_customer is None:
			raise ValidationError('Customer must be specified')


class ProductImage(AbstractBase): 
	# https://docs.djangoproject.com/en/3.2/ref/models/fields/#django.db.models.FileField
	ref_product = models.ForeignKey('ProductItem', on_delete=models.CASCADE, null=True)

	def product_directory_path(instance, filename):
		# file will be uploaded to MEDIA_ROOT/product_<id>/<filename>
		return 'product_{0}/{1}'.format(instance.ref_product.id, filename)

	product_image = models.ImageField(upload_to=product_directory_path, null=True)

	def clean(self):
		super().clean()
		if self.ref_product is None or self.product_image is None:
			raise ValidationError('Product and image must be specified')

	def __str__(self):
		return self.name


class OrderStatus(AbstractStatusBase):
	class Meta():
		verbose_name_plural = "OrderStatuses"

	def clean(self):
		super().clean()
		if self.name is None:
			raise ValidationError('Name must be specified')

class DeliveryOption(AbstractBase):
	price_of_delivery = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	duration_days = models.IntegerField(null=True)
	# responsible: ?? ## if we want to follow up the delivery and inform the client - need further data, if we want this only for a choice option - we can go fine with existing props

	def clean(self):
		super().clean()
		if self.name is None:
			raise ValidationError('Name must be specified')

#-------------------------------- Marketing 

class Rebate(AbstractBase):
	discount_mutiplicator = models.DecimalField(max_digits=3, decimal_places=2, null=True)
	free_shipping = models.BooleanField(default=False)
	ref_product = models.ForeignKey('ProductItem', on_delete=models.CASCADE, null=True) # rebate for a product
	ref_productCategory = models.ManyToManyField('ProductCategory') # rebate for a product category
	ref_customerGroup = models.ManyToManyField('CustomerCategory') 

	def clean(self):
		super().clean()
		if self.discount_mutiplicator is None and self.free_shipping is not True:
			raise ValidationError('Discount or free shipping must be specified')

	def __str__(self):
		return '{0} | discount {1}% | free shipping: {2}'.format(self.name, (self.discount_mutiplicator * 100) , self.free_shipping) 
	

class RebateAction(AbstractBase):
	ref_rebate = models.ForeignKey('Rebate', on_delete=models.CASCADE, null=True) # which rebate
	date_from = models.DateTimeField(null=True)
	dateTo = models.DateTimeField(null=True)
	is_promo_code_action = models.BooleanField(default=False) # rebate applied per default or only if Promocode was applied 
	from_SU_quantity = models.IntegerField(null=True) # apllied from a specified selling-unit quantity (not less)
	toSuQuantity = models.IntegerField(null=True)  # apllied until a specified selling-unit quantity (not more)

	def clean(self):
		super().clean()
		if self.ref_rebate is None:
			raise ValidationError('Rebate must be specified')

	def __str__(self):
		return '{0} | {1}'.format(self.name, self.ref_rebate) 


class MailingAction(AbstractBase):
	url_token = models.CharField(max_length=200, null=True) # ecrypted url token for marketing analysis - how many people followed the link for example
	number_of_links_sent =  models.IntegerField(null=True)
	ref_rebate_action = models.ForeignKey('RebateAction', on_delete=models.SET_NULL, null=True) # which rebate action we are promoting
	ref_customer_group = models.ForeignKey('CustomerCategory', on_delete=models.SET_NULL, null=True) # to whom are we mailing?
	ref_message = models.ForeignKey('MailMessage', on_delete=models.SET_NULL, null=True) # what are we mailing?

	def clean(self):
		super().clean()
		if self.ref_message is None:
			raise ValidationError('Message must be specified')

	def __str__(self):
		return self.name


class MailMessage(AbstractBase):
	message_subject = models.CharField(max_length=200, null=True)
	message_text = models.TextField(default="")

	def clean(self):
		super().clean()
		if self.message_subject is None or self.message_text is None:
			raise ValidationError('Message text and subject must be specified')
	
	def __str__(self):
		return self.message_subject


class UserCorrespondence(AbstractBase):
	ref_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
	ref_message = models.ForeignKey('MailMessage', on_delete=models.PROTECT, null=True)
	ref_type_of_message = models.ForeignKey('TypeOfCorrespondence', on_delete=models.SET_NULL, null=True)

	class Meta():
		verbose_name_plural = "UserCorrespondence"

	def clean(self):
		super().clean()
		if self.ref_user is None:
			raise ValidationError('Sender or Reciever (USER) must be specified')
		# eine Konstante in settings setzen und sie als absender eintragen wenn ausgehende Kommunikation

	def __str__(self):
		return 'Incoming: {0} | {1}'.format(ref_user.get_username(), self.ref_message.message_subject)


class TypeOfCorrespondence(AbstractStatusBase):
	def __str__(self):
		return self.name
	def clean(self):
		super().clean()
		if self.name is None:
			raise ValidationError('Name must be specified')
	class Meta():
		verbose_name_plural = "TypesOfCorrespondence"


class LinkFollowup(AbstractBase):
	ref_mailing_action = models.OneToOneField('MailingAction', on_delete=models.CASCADE, null=True)
	visits_quanitiy = models.IntegerField(default=0)
	followup_orders_quantity = models.IntegerField(default=0) # how many orders was placed during the followup session
	followup_turnover = models.DecimalField( max_digits=10, decimal_places=2, default=0.00) # how much turnover was made during the followup session

	def clean(self):
		super().clean()
		if self.ref_mailing_action is None:
			raise ValidationError('Mailing Action must be specified')

	def __str__(self):
		return 'Followup: {0} '.format(self.ref_mailing_action)


class PromoCodeAction(AbstractBase):
	promocode = models.CharField(max_length=50, null=True)
	ref_rebate_action =  models.ForeignKey('RebateAction', on_delete=models.CASCADE, null=True)
	followup_orders_quantity = models.IntegerField(default=0) # how many orders was placed with this promocode
	followup_turnover = models.DecimalField( max_digits=10, decimal_places=2, default=0.00) # how much turnover was made  with this promocode

	def clean(self):
		super().clean()
		if self.ref_mailing_action is None:
			raise ValidationError('Mailing Action must be specified')

	def __str__(self):
		return self.name


#---------------------------------- feedback und returns

class ProductReview(AbstractBase):
	ref_product = models.ForeignKey('ProductItem', on_delete=models.CASCADE, null=True)
	ref_customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True) # Was genau wollen wir hier on_delete machen und wie ist es mit datenschutz?
	is_confirmed_buyer = models.BooleanField(default=False)
	review_text = models.TextField(null=True)
	# rating: ??????? string | number ? or reference to a Rating Class? 
	
	def user_images_path(instance, filename):
		# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
		return 'user_{0}/{1}'.format(instance.ref_customer.ref_user.id, filename)

	review_image =  models.ImageField(null=True, upload_to=user_images_path)

	def clean(self):
		super().clean()
		if self.ref_product is None:
			raise ValidationError('Product must be specified')
		if self.ref_customer is None:
			raise ValidationError('Customer must be specified')
	

class ProductReturn(AbstractBase):
	ref_product_order = models.ForeignKey('ProductOrder', on_delete=models.SET_NULL, null=True)
	quantity_SU_returned = models.IntegerField(null=True)
	reason_for_return = models.CharField(max_length=200, null=True) ## later we can do return followup and processing classes to give it a glance
	additional_feedback = models.TextField(null=True)
	date_of_return = models.DateTimeField(auto_now_add=True, null=True)
	ref_return_status = models.ForeignKey('ReturnStatus', on_delete=models.SET_NULL, null=True)

	def clean(self):
		super().clean()
		if self.ref_product_order is None:
			raise ValidationError('ProductOrder must be specified')


class ReturnStatus(AbstractStatusBase):
	class Meta():
		verbose_name_plural = "ReturnStatuses"

	def clean(self):
		super().clean()
		if self.name is None:
			raise ValidationError('Name must be specified')
