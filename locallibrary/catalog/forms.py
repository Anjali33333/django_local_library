from django import forms
import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text="Enter a date within the next 4 weeks (default is 3 weeks from today)."
    )

    def clean_renewal_date(self):
        data = self.cleaned_data["renewal_date"]

        # Check if the date is not in the past
        if data < datetime.date.today():
            raise forms.ValidationError("Invalid date - renewal in past")

        # Check if the date is in the allowed range (4 weeks max)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise forms.ValidationError("Invalid date - renewal more than 4 weeks ahead")

        return data
