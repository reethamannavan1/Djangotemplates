from django import forms
from .models import Enrollment, Course


class EnrollmentForm(forms.ModelForm):

    # optional fields
    last_name = forms.CharField(required=False)
    message = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Enrollment
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "gender",
            "dob",
            "address",
            "city",
            "state",
            "pincode",
            "course",
            "mode",
            "message",
        ]


    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Enter a valid 10-digit phone number.")
        return phone

    def clean_pincode(self):
        pincode = self.cleaned_data["pincode"]
        if not pincode.isdigit() or len(pincode) != 6:
            raise forms.ValidationError("Enter a valid 6-digit pincode.")
        return pincode
