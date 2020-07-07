import json
import requests
from threading import Timer
from QBesharatSolution import settings
from jalali_date import datetime2jalali
from django.utils.translation import ugettext_lazy as _


def to_jalali_full(date):
    return datetime2jalali(date).strftime('%H:%M:%S %Y/%m/%d')


def switch_lang_code(path, language):
    # Get the supported language codes
    lang_codes = [c for (c, name) in settings.LANGUAGES]

    # Validate the inputs
    if path == '':
        raise Exception('URL path for language switch is empty')
    elif path[0] != '/':
        raise Exception('URL path for language switch does not start with "/"')
    elif language not in lang_codes:
        raise Exception('%s is not a supported language code' % language)

    # Split the parts of the path
    parts = path.split('/')

    # Add or substitute the new language prefix
    if parts[1] in lang_codes:
        parts[1] = language
    else:
        parts[0] = "/" + language

    # Return the full new path
    return '/'.join(parts)


def get_admin_url(self):
    """the url to the Django admin interface for the model instance"""
    from django.urls import reverse

    info = (self._meta.app_label, self._meta.model_name)
    return reverse('admin:%s_%s_change' % info, args=(self.pk,))


key = 'online_support_status'
_online_support = None


def online_support(request):
    global _online_support
    if not _online_support:
        update_online_support(request)

    return _online_support


def update_online_support(request):
    global _online_support
    try:
        url = '%sapi/operator/status/' % settings.CHAT_SERVER_URL
        response = requests.get(url)
        _online_support = json.loads(response.content)
    except:
        _online_support = False
    finally:
        r = Timer(settings.CHAT_SUPPORT_REFRESH_INTERVAL, update_online_support, args=(request,))
        r.start()


def update_operator(request, status):
    data = {'name': request.user.pk, 'status': status}
    url = '%sapi/operator/' % settings.CHAT_SERVER_URL
    try:
        response = requests.patch(url, data=data)
        if response.status_code == 200:
            request.session['operator'] = json.loads(response.content)
            update_online_support(request)
    except:
        raise Exception(_('Error in updating online support operator'))


def get_operator(request, create=False):
    data = {'name': request.user.pk}
    url = '%sapi/operator/' % settings.CHAT_SERVER_URL
    try:
        response = requests.get(url, data=data)
        if response.status_code == 200:
            request.session['operator'] = json.loads(response.content)
        elif create:
            register_operator(request, request.user)
    except Exception as e:
        raise Exception(_('Error in getting online support operator'))


def register_operator(request, user):
    url = '%sapi/operator/' % settings.CHAT_SERVER_URL
    data = {'name': user.pk, }
    try:
        response = requests.post(url, data=data)
        if response.status_code in [200, 201]:
            request.session['operator'] = json.loads(response.content)
            update_online_support(request)
        else:
            raise Exception(response.content.decode(), True)
    except Exception as e:
        if e.args[1]:
            raise Exception(e.args[0])
        else:
            raise Exception(_('Subscribing user in chat server failed. Try later'))


def unregister_operator(request, user):
    url = '%sapi/operator/0/' % settings.CHAT_SERVER_URL
    data = {'name': user.pk, }
    try:
        response = requests.delete(url, data=data)
        if response.status_code in [200, 201]:
            if 'operator' in request.session: del request.session['operator']
            update_online_support(request)
        else:
            raise Exception(response.content.decode(), True)
    except Exception as e:
        if e.args[1]:
            raise Exception(e.args[0])
        else:
            raise Exception(_('Unsubscribing user from chat server failed. Try later'))
