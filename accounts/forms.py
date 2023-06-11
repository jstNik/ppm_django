from django.contrib.auth.forms import UserCreationForm
from django import forms
from string import Template

from django.forms import ClearableFileInput
from django.utils.safestring import mark_safe
from accounts.models import Account


class DateInput(forms.DateInput):
    input_type = 'date'


class RemoveFreeText(ClearableFileInput):
    initial_text = None
    template_name = 'widgets/my_clearable_file_input.html'
    input_text = None
    clear_checkbox_label = None
    show_image_link = False


class AccountEditForm(forms.ModelForm):
    birthday = forms.DateField(required=False, widget=DateInput)
    profile_picture = forms.ImageField(required=False, widget=RemoveFreeText)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'email', 'bio', 'birthday', 'profile_picture']


class AccountSignupForm(UserCreationForm):
    birthday = forms.DateField(required=False, widget=DateInput)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = Account
        fields = [
            'first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'birthday', 'profile_picture']


class DeletionForm(forms.Form):
    delete = forms.CharField(max_length=10, required=False)

    def clean_delete(self):
        data = self.cleaned_data.get('delete')
        if data == 'delete':
            return data
        raise forms.ValidationError('The text doesn\'t match.')
