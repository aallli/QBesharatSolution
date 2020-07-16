from QBesharat.forms import *
from django.contrib import admin
from django.conf import settings
from django.contrib import messages
from django_summernote.models import Attachment
from django.contrib.auth.admin import UserAdmin
from jalali_date.admin import ModelAdminJalaliMixin
from django.utils.translation import ugettext_lazy as _
from QBesharatSolution.utlis import register_operator, unregister_operator
from QBesharat.models import User, City, Country, Memorizer, Qari, Concepts, Tutor


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


class MemorizerInline(admin.StackedInline):
    model = Memorizer
    fields = [('parts', 'awards', 'certificates'), ]
    insert_after_fieldset = _('Address Info')


class QariInline(admin.StackedInline):
    model = Qari
    fields = [('fluent_reading', 'tahdir', 'tartil', 'research'), 'courses', 'awards', 'certificates']
    form = QariInlineForm
    insert_after_fieldset = _('Address Info')


class ConceptsInline(admin.StackedInline):
    model = Concepts
    fields = [('interpretation', 'translation'), ]
    form = ConceptsInlineForm
    insert_after_fieldset = _('Address Info')


class TutorInline(admin.StackedInline):
    model = Tutor
    fields = [('grade', 'course_duration', 'course_content'), 'courses', 'awards', 'certificates']
    insert_after_fieldset = _('Address Info')


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
            'fields': (('last_login_jalali', 'date_joined_jalali'),)}),
        (_('Permissions'), {
            'fields': (('is_staff', 'is_superuser'), 'groups', 'user_permissions'), }),
        (_('Sensitive Info'), {'fields': ('password',)}),
    )
    list_filter = ('country', 'city', 'sex', 'is_active', 'registered', 'is_superuser', 'groups')
    form = UserForm
    readonly_fields = ['image_tag', 'last_login_jalali', 'date_joined_jalali']
    inlines = [MemorizerInline, QariInline, ConceptsInline, TutorInline]
    change_form_template = 'admin/custom/change_form.html'

    def save_form(self, request, form, change):
        try:
            user = form.instance
            if 'groups' in form.changed_data:
                if form.cleaned_data['groups'].filter(
                        name=settings.CHAT_SUPPORT_GROUP).count() == 1 and \
                                user.groups.filter(name=settings.CHAT_SUPPORT_GROUP).count() == 0:
                    register_operator(request, user)

                elif user.groups.filter(name=settings.CHAT_SUPPORT_GROUP).count() == 1:
                    unregister_operator(request, user)
            return super(UserAdmin, self).save_form(request, form, change)
        except Exception as e:
            self.message_user(request, e, level=messages.ERROR)


admin.site.unregister(Attachment)
