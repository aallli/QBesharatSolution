import os
import base64
import locale
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from QBesharatSolution import settings
from django.utils.html import mark_safe
from QBesharat.utils import to_jalali_full
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from QBesharatSolution.utlis import get_admin_url

locale.setlocale(locale.LC_ALL, '')


def hide_title(class_name):
    return '<script type="text/javascript">document.getElementsByClassName("%s")[0].style.display = "none";</script>' % class_name


class Sex(models.TextChoices):
    PROFILE_SEX_MALE = 'male', _('Male')
    PROFILE_SEX_FEMALE = 'female', _('Female')


class Country(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=200, unique=True, null=False)
    active = models.BooleanField(verbose_name=_('Active'), default=True)

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
        ordering = ['name']

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class City(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=200, unique=True, null=False)
    country = models.ForeignKey(Country, verbose_name=_('Country'), on_delete=models.CASCADE)
    active = models.BooleanField(verbose_name=_('Active'), default=True)

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")
        ordering = ['name']

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class User(AbstractUser):
    mobile_regex = RegexValidator(
        regex=r'^\d{9,15}$',
        message=_('Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.'))
    mobile = models.CharField(verbose_name=_('Mobile'), validators=[mobile_regex], max_length=17, blank=True, null=True,
                              unique=True)
    sex = models.CharField(verbose_name=_('Sex'), choices=Sex.choices, default=Sex.PROFILE_SEX_FEMALE, max_length=10,
                           null=False)
    country = models.ForeignKey(Country, verbose_name=_('Country'), on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, verbose_name=_('City'), on_delete=models.SET_NULL, null=True, blank=True)
    birth_date = models.DateField(verbose_name=_('Birth Date'), null=True, blank=True, default='1980-01-01')
    image = ResizedImageField(size=[settings.MAX_SMALL_IMAGE_WIDTH, settings.MAX_SMALL_IMAGE_HEIGHT],
                              verbose_name=_('Profile Image'), upload_to=settings.MEDIA_URL[1:len(settings.MEDIA_URL)],
                              blank=True, null=True)
    otp = models.CharField(verbose_name='OTP', max_length=30, null=True, blank=True)
    otp_creation_date = models.DateTimeField(verbose_name=_('OTP Creation Date'), null=True, blank=True)
    password_reset_otp = models.CharField(verbose_name=_('Password Reset OTP'), max_length=30, null=True, blank=True)
    password_reset_otp_creation_date = models.DateTimeField(verbose_name=_('Password Reset OTP Creation Date'),
                                                            null=True,
                                                            blank=True)
    registered = models.BooleanField(verbose_name=_('Registered'), default=False)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return self.get_full_name() or self.get_username()

    def __unicode__(self):
        return self.get_full_name() or self.get_username()

    @property
    def image_data(self):
        if self.image:
            self.image.open()
            return 'data:image/jpeg;base64,%s' % base64.b64encode(self.image.read()).decode("utf-8")
        else:
            return None

    def image_tag(self):
        if self.image:
            return mark_safe(
                '<a href="%s%s" target="_blank"><img src="%s%s" title="%s" alt="%s" style="max-width:%spx;max-height:%spx;"/></a>' % (
                    settings.MEDIA_URL, self.image, settings.MEDIA_URL, self.image, self, self,
                    settings.MAX_SMALL_IMAGE_WIDTH, settings.MAX_SMALL_IMAGE_HEIGHT))
        else:
            return mark_safe('<img src="%simg/person-icon.jpg" width="150" height="150" title="%s" alt="%s"/>' % (
                settings.STATIC_URL, self.name, self.name))

    image_tag.short_description = _('Image')


@receiver(models.signals.post_delete, sender=User)
def auto_delete_brand_image_on_delete(sender, instance, **kwargs):
    """
    Deletes image from filesystem
    when corresponding `User` object is deleted.
    """
    if instance.image.name:
        try:
            if os.path.isfile(instance.image.path):
                os.remove(instance.image.path)
        except Exception as e:
            print('Delete error: %s' % e.args[0])


@receiver(models.signals.pre_save, sender=User)
def auto_delete_brand_image_on_change(sender, instance, **kwargs):
    """
    Deletes old image from filesystem
    when corresponding `User` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_image = User.objects.get(pk=instance.pk).image
    except User.DoesNotExist:
        return False

    if not old_image.name:
        return False

    new_image = instance.image
    try:
        if not old_image == new_image:
            if os.path.isfile(old_image.path):
                os.remove(old_image.path)
    except Exception as e:
        print('Delete error: %s' % e.args[0])
        return False
