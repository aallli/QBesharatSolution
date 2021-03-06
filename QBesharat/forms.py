from django.contrib.auth.forms import UserChangeForm
from django import forms
from QBesharat.models import User, City


class UserForm(UserChangeForm):
    class Meta:
        model = User
        exclude = []

    class Media:
        css = {'all': ('css/custom_user_admin.css',)}
        js = ('js/custom_user_admin.js',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.filter(country=self.instance.country)

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = City.objects.filter(country=self.instance.country)


class QariInlineForm(forms.ModelForm):
    class Meta:
        widgets = {
            'fluent_reading': forms.CheckboxInput(attrs={'style': 'width:20px;height:20px;'}),
            'tahdir': forms.CheckboxInput(attrs={'style': 'width:20px;height:20px;'}),
            'tartil': forms.CheckboxInput(attrs={'style': 'width:20px;height:20px;'}),
            'research': forms.CheckboxInput(attrs={'style': 'width:20px;height:20px;'}),
        }


class ConceptsInlineForm(forms.ModelForm):
    class Meta:
        widgets = {
            'interpretation': forms.CheckboxInput(attrs={'style': 'width:20px;height:20px;'}),
            'translation': forms.CheckboxInput(attrs={'style': 'width:20px;height:20px;'}),
        }
