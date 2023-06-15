from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.utils.translation import gettext_lazy as _
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


class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, label="Username or email")
    error_messages = {
        "invalid_login": _(
            "Please enter a correct username/email and password."
        ),
        "inactive": _("This account is inactive."),
    }


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
