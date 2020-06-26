from QBesharat.forms import *
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.admin import UserAdmin
from django_summernote.models import Attachment
from QBesharat.models import User, City, Country
from jalali_date.admin import ModelAdminJalaliMixin
from django.utils.translation import ugettext_lazy as _


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


class BaseModelAdmin(admin.ModelAdmin):
    list_per_page = settings.LIST_PER_PAGE
    save_on_top = True

    class Media:
        js = ('js/custom_admin.js',)


class CityInline(admin.TabularInline):
    model = City


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    fields = ['name', 'active']
    list_display = ['name', 'active']
    list_display_links = ['name', 'active']
    model = Country
    list_filter = ['active']
    search_fields = ['name', ]
    inlines = [CityInline, ]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    fields = ['name', 'country', 'active']
    list_display = ['name', 'country', 'active']
    list_display_links = ['name', 'country', 'active']
    model = City
    list_filter = ['country', 'active']
    search_fields = ['name', 'country__name']


@admin.register(User)
class UserAdmin(ModelAdminJalaliMixin, UserAdmin, BaseModelAdmin):
    fieldsets = (
        (_('Personal info'), {
            'fields': (('username', 'first_name', 'last_name'),
                       ('image', 'image_tag'),
                       ('sex', 'birth_date', 'is_active', 'registered'),)}),
        (_('Address Info'), {
            'fields': (('mobile', 'email'), ('country', 'city'))}),
        (_('Important dates'), {
            'fields': (('last_login', 'date_joined'))}),
        (_('Permissions'), {
            'fields': (('is_staff', 'is_superuser'), 'groups', 'user_permissions'), }),
        (_('Sensitive Info'), {'fields': ('password',)}),
    )
    list_filter = ('country', 'city', 'sex', 'is_active', 'registered', 'is_superuser', 'groups')
    form = UserForm
    readonly_fields = ['image_tag']


admin.site.unregister(Attachment)
