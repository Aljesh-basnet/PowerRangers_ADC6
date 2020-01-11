from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import *
from django.utils.encoding import python_2_unicode_compatible
from django_libs.models_mixins import TranslationModelMixin
from django_countries.fields import CountryField
from hvad.models import TranslatableModel, TranslatedFields

class BookRoom(models.Model):
    cname = models.CharField(max_length=20)
    roomtype =models.CharField(max_length=20)
    roomno=models.IntegerField()
    cemail = models.EmailField()
    ccontact = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.cname} has booked {self.roomno}"




class BookingStatus(TranslationModelMixin, TranslatableModel):
   
    slug = models.SlugField(
        verbose_name=_('Slug'),
    )

    translations = TranslatedFields(
        name=models.CharField(
            verbose_name=_('Name'),
            max_length=128,
        )
    )

class Booking(models.Model):
    
    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('User'),
        related_name='bookings',
        blank=True, null=True,
    )

    session = models.ForeignKey(
        'sessions.Session',
        verbose_name=_('Session'),
        blank=True, null=True,
    )

    title = models.CharField(
        max_length=10,
        verbose_name=_('Title'),
        choices=(
            ('dr', _('Dr.')),
            ('prof', _('Prof.')),
        ),
        blank=True,
    )

    forename = models.CharField(
        verbose_name=_('First name'),
        max_length=20,
        blank=True,
    )

    surname = models.CharField(
        verbose_name=_('Last name'),
        max_length=20,
        blank=True,
    )

    nationality = CountryField(
        max_length=2,
        verbose_name=_('Nationality'),
        blank=True,
    )

    street1 = models.CharField(
        verbose_name=_('Street 1'),
        max_length=256,
        blank=True,
    )

    street2 = models.CharField(
        verbose_name=_('Street 2'),
        max_length=256,
        blank=True,
    )

    city = models.CharField(
        verbose_name=_('City'),
        max_length=256,
        blank=True,
    )

    zip_code = models.CharField(
        verbose_name=_('ZIP/Postal code'),
        max_length=256,
        blank=True,
    )

    country = CountryField(
        max_length=2,
        verbose_name=_('Country'),
        blank=True,
    )

    email = models.EmailField(
        verbose_name=_('Email'),
        blank=True,
    )

    phone = models.CharField(
        verbose_name=_('Phone'),
        max_length=256,
        blank=True,
    )

    special_request = models.TextField(
        max_length=1024,
        verbose_name=_('Special request'),
        blank=True,
    )

    date_from = models.DateTimeField(
        verbose_name=_('From'),
        blank=True, null=True,
    )

    date_until = models.DateTimeField(
        verbose_name=_('Until'),
        blank=True, null=True,
    )

    creation_date = models.DateTimeField(
        verbose_name=_('Creation date'),
        auto_now_add=True,
    )

    booking_id = models.CharField(
        max_length=100,
        verbose_name=_('Booking ID'),
        blank=True,
    )

    booking_status = models.ForeignKey(
        'booking.BookingStatus',
        verbose_name=('Booking status'),
        blank=True, null=True,
    )

    notes = models.TextField(
        max_length=1024,
        verbose_name=('Notes'),
        blank=True,
    )

    time_period = models.PositiveIntegerField(
        verbose_name=_('Time period'),
        blank=True, null=True,
    )

    time_unit = models.CharField(
        verbose_name=_('Time unit'),
        default=getattr(settings, 'BOOKING_TIME_INTERVAL', ''),
        max_length=64,
        blank=True,
    )

    total = models.DecimalField(
        max_digits=36,
        decimal_places=2,
        verbose_name=_('Total'),
        blank=True, null=True,
    )

    currency = models.CharField(
        verbose_name=_('Currency'),
        max_length=128,
        blank=True,
    )

    class Meta:
        ordering = ['-creation_date']

    def __str__(self):
        return '#{} ({})'.format(self.booking_id or self.pk,
                                 self.creation_date)


class BookingError(models.Model):
    booking = models.ForeignKey(
        Booking,
        verbose_name=_('Booking'),
    )
    message = models.CharField(
        verbose_name=_('Message'),
        max_length=1000,
        blank=True,
    )
    details = models.TextField(
        verbose_name=_('Details'),
        max_length=4000,
        blank=True,
    )

    date = models.DateTimeField(
        verbose_name=_('Date'),
        auto_now_add=True,
    )

    def __str__(self):
        return u'[{0}] {1} - {2}'.format(self.date, self.booking.booking_id,
                                         self.message)

class BookingItem(models.Model):
  
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_('Quantity'),
    )

    persons = models.PositiveIntegerField(
        verbose_name=_('Persons'),
        blank=True, null=True,
    )

    subtotal = models.DecimalField(
        max_digits=36,
        decimal_places=2,
        verbose_name=_('Subtotal'),
        blank=True, null=True,
    )

    # GFK 'booked_item'
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    booked_item = GenericForeignKey('content_type', 'object_id')

    booking = models.ForeignKey(
        'booking.Booking',
        verbose_name=_('Booking'),
    )

    class Meta:
        ordering = ['-booking__creation_date']

    def __str__(self):
        return u'{} ({})'.format(self.booking, self.booked_item)

    @property
    def price(self):
        return self.quantity * self.subtotal

class ExtraPersonInfo(models.Model):
    forename = models.CharField(
        verbose_name=_('First name'),
        max_length=20,
    )

    surname = models.CharField(
        verbose_name=_('Last name'),
        max_length=20,
    )

    arrival = models.DateTimeField(
        verbose_name=_('Arrival'),
        blank=True, null=True,
    )

    message = models.TextField(
        max_length=1024,
        verbose_name=_('Message'),
        blank=True,
    )

    class Meta:
        ordering = ['-booking__creation_date']

    def __str__(self):
        return u'{} {} ({})'.format(self.forename, self.surname, self.booking)
