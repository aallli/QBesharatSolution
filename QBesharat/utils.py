from jalali_date import datetime2jalali
from django.utils.translation import ugettext_lazy as _


def to_jalali_full(date):
    return datetime2jalali(date).strftime('%H:%M:%S %Y/%m/%d')


msgid = _("welcome")
msgid = _("Admin Interface")
msgid = _("Django Summernote")
msgid = _("Theme")
msgid = _("Themes")
msgid = _("Attachment")
msgid = _("Attachments")
msgid = _("Email address")
msgid = _('Hold down “Control”, or “Command” on a Mac, to select more than one.')
msgid = _('First, enter a username and password. Then, you’ll be able to edit more user options.')
msgid = _(
    'Raw passwords are not stored, so there is no way to see this '
    'user’s password, but you can change the password using '
    '<a href="{}">this form</a>.'
)
