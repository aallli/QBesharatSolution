import os, base64, locale
from django.db import models
from django.dispatch import receiver
from QBesharatSolution import settings
from django.utils.html import mark_safe
from django_resized import ResizedImageField
from django.core.validators import RegexValidator
from QBesharatSolution.utlis import to_jalali_full
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

locale.setlocale(locale.LC_ALL, '')


def hide_title(class_name):
    return '<script type="text/javascript">document.getElementsByClassName("%s")[0].style.display = "none";</script>' % class_name


class Sex(models.TextChoices):
    PROFILE_SEX_MALE = 'male', _('Male')
    PROFILE_SEX_FEMALE = 'female', _('Female')


class Topic(models.Model):
    description = models.CharField(verbose_name=_('Description'), max_length=2000, unique=True, null=False)
    active = models.BooleanField(verbose_name=_('Active'), default=True)

    class Meta:
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")
        ordering = ['description']

    def __str__(self):
        return '%s...' % self.description[:25]

    def __unicode__(self):
        return '%s...' % self.description[:25]


class Subject(models.Model):
    topic = models.ForeignKey(Topic, verbose_name=_('Topic'), on_delete=models.CASCADE)
    description = models.TextField(verbose_name=_('Description'), max_length=2000, null=False)
    verse = models.TextField(verbose_name=_('Verse'), max_length=2000, unique=True, null=False)
    date = models.DateField(verbose_name=_('Date'), null=True, blank=False, default='1399-04-01')
    active = models.BooleanField(verbose_name=_('Active'), default=True)

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")
        ordering = ['description']
        unique_together = ['topic', 'description']

    def __str__(self):
        return '%s: %s' % (self.topic, self.description)

    def __unicode__(self):
        return '%s: %s' % (self.topic, self.description)

    def date_jalali(self):
        return to_jalali_full(self.date, True)

    date_jalali.short_description = _('Date')


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
    birth_date = models.DateField(verbose_name=_('Birth Date'), null=True, blank=True, default='1360-01-01')
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

    def last_login_jalali(self):
        return to_jalali_full(self.last_login)

    last_login_jalali.short_description = _('last login')

    def date_joined_jalali(self):
        return to_jalali_full(self.date_joined)

    date_joined_jalali.short_description = _('date joined')

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


class Memorizer(models.Model):
    user = models.OneToOneField(User, verbose_name=_('Memorizer skill'), on_delete=models.CASCADE)
    parts = models.IntegerField(verbose_name=_('Parts'), validators=[MinValueValidator(1), MaxValueValidator(30)],
                                blank=True, null=True)
    awards = models.CharField(verbose_name=_('Awards'), max_length=500, blank=True, null=True)
    certificates = models.CharField(verbose_name=_('Certificates'), max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = _("Memorizer skill")
        verbose_name_plural = _("Memorizers skill")


class Qari(models.Model):
    user = models.OneToOneField(User, verbose_name=_('Qari skill'), on_delete=models.CASCADE)
    fluent_reading = models.BooleanField(verbose_name=_('Fluent Reading'), blank=True, null=True)
    tahdir = models.BooleanField(verbose_name=_('Tahdir'), blank=True, null=True)
    tartil = models.BooleanField(verbose_name=_('Tartil'), blank=True, null=True)
    research = models.BooleanField(verbose_name=_('Research'), blank=True, null=True)
    courses = models.CharField(verbose_name=_('Courses'), max_length=500, blank=True, null=True)
    awards = models.CharField(verbose_name=_('Awards'), max_length=500, blank=True, null=True)
    certificates = models.CharField(verbose_name=_('Certificates'), max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = _("Qari skill")
        verbose_name_plural = _("Qari skill")


class Concepts(models.Model):
    user = models.OneToOneField(User, verbose_name=_('Concepts skill'), on_delete=models.CASCADE)
    interpretation = models.BooleanField(verbose_name=_('Interpretation'), blank=True, null=True)
    translation = models.BooleanField(verbose_name=_('Translation'), blank=True, null=True)

    class Meta:
        verbose_name = _("Concepts skill")
        verbose_name_plural = _("Concepts skill")


class Tutor(models.Model):
    user = models.OneToOneField(User, verbose_name=_('Tutor skill'), on_delete=models.CASCADE)
    grade = models.IntegerField(verbose_name=_('Grade'), validators=[MinValueValidator(1), MaxValueValidator(10)],
                                blank=True, null=True)
    course_duration = models.IntegerField(verbose_name=_('Course duration'),
                                          validators=[MinValueValidator(1), MaxValueValidator(400)],
                                          blank=True, null=True)
    course_content = models.CharField(verbose_name=_('Course Content'), max_length=2000, blank=True, null=True)
    courses = models.CharField(verbose_name=_('Courses'), max_length=500, blank=True, null=True)
    awards = models.CharField(verbose_name=_('Awards'), max_length=500, blank=True, null=True)
    certificates = models.CharField(verbose_name=_('Certificates'), max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = _("Tutor skill")
        verbose_name_plural = _("Tutors skill")


class Network(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=200, unique=True, null=False)
    active = models.BooleanField(verbose_name=_('Active'), default=True)

    class Meta:
        verbose_name = _("Network")
        verbose_name_plural = _("Networks")
        ordering = ['name']

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Program(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=1000, unique=True, null=False)
    network = models.ForeignKey(Network, verbose_name=_('Network'), on_delete=models.CASCADE)
    poster = ResizedImageField(size=[settings.MAX_MEDIUM_IMAGE_WIDTH, settings.MAX_MEDIUM_IMAGE_HEIGHT],
                              verbose_name=_('Poster'), upload_to=settings.MEDIA_URL[1:len(settings.MEDIA_URL)],
                              blank=True, null=True)
    count = models.IntegerField(verbose_name=_('Count'), default=60, blank=False)
    active = models.BooleanField(verbose_name=_('Active'), default=True)

    class Meta:
        verbose_name = _("Program")
        verbose_name_plural = _("Programs")
        ordering = ['network', 'name']

    def __str__(self):
        return '%s: %s' % (self.network, self.name)

    def __unicode__(self):
        return '%s: %s' % (self.network, self.name)

    def production_date_jalali(self):
        return to_jalali_full(self.production_date, True)

    production_date_jalali.short_description = _('Production Date')

    @property
    def poster_data(self):
        if self.poster:
            self.poster.open()
            return 'data:image/jpeg;base64,%s' % base64.b64encode(self.poster.read()).decode("utf-8")
        else:
            return None

    def poster_tag(self):
        if self.poster:
            return mark_safe(
                '<a href="%s%s" target="_blank"><img src="%s%s" title="%s" alt="%s" style="max-width:%spx;max-height:%spx;"/></a>' % (
                    settings.MEDIA_URL, self.poster, settings.MEDIA_URL, self.poster, self, self,
                    settings.MAX_SMALL_IMAGE_WIDTH, settings.MAX_SMALL_IMAGE_HEIGHT))
        else:
            return mark_safe('<img src="%simg/person-icon.jpg" width="150" height="150" title="%s" alt="%s"/>' % (
                settings.STATIC_URL, self.name, self.name))


@receiver(models.signals.post_delete, sender=Program)
def auto_delete_program_image_on_delete(sender, instance, **kwargs):
    """
    Deletes poster from filesystem
    when corresponding `Program` object is deleted.
    """
    if instance.poster.name:
        try:
            if os.path.isfile(instance.poster.path):
                os.remove(instance.poster.path)
        except Exception as e:
            print('Delete error: %s' % e.args[0])


@receiver(models.signals.pre_save, sender=Program)
def auto_delete_program_image_on_change(sender, instance, **kwargs):
    """
    Deletes old poster from filesystem
    when corresponding `Program` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_poster = Program.objects.get(pk=instance.pk).poster
    except Program.DoesNotExist:
        return False

    if not old_poster.name:
        return False

    new_poster = instance.poster
    try:
        if not old_poster == new_poster:
            if os.path.isfile(old_poster.path):
                os.remove(old_poster.path)
    except Exception as e:
        print('Delete error: %s' % e.args[0])
        return False


class Episod(models.Model):
    program = models.ForeignKey(Program, verbose_name=_('Program'), on_delete=models.CASCADE)
    publish_date = models.DateField(verbose_name=_('Publish Date'), null=True, blank=True, default='1399-04-01')
    duration = models.IntegerField(verbose_name=_('Duration (min)'), default=30, blank=False) # in minutes
    active = models.BooleanField(verbose_name=_('Active'), default=True)

    class Meta:
        verbose_name = _("Episod")
        verbose_name_plural = _("Episods")
        ordering = ['publish_date']

    def __str__(self):
        return '%s (%s)' % (self.program, self.publish_date_jalali())

    def __unicode__(self):
        return '%s (%s)' % (self.program, self.publish_date_jalali())

    def publish_date_jalali(self):
        return to_jalali_full(self.publish_date, True)

    publish_date_jalali.short_description = _('Publish Date')


class Platform(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=200, unique=True, null=False)
    active = models.BooleanField(verbose_name=_('Active'), default=True)

    class Meta:
        verbose_name = _("Platform")
        verbose_name_plural = _("Platforms")
        ordering = ['name']

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class EndPoint(models.Model):
    platform = models.ForeignKey(Platform, verbose_name=_('Platform'), on_delete=models.CASCADE)
    url = models.CharField(verbose_name=_('URL'), max_length=2000, unique=True, null=False)
    active = models.BooleanField(verbose_name=_('Active'), default=True)
    episod = models.ForeignKey(Episod, verbose_name=_('Episod'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("EndPoint")
        verbose_name_plural = _("EndPoint")
        ordering = ['platform', 'url']

    def __str__(self):
        return self.platform.name

    def __unicode__(self):
        return self.platform.name

