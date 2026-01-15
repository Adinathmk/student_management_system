from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class StudentRegisterForm(UserCreationForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "phone",
            "date_of_birth",
            "gender",
            "profile_picture",
            "is_active",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].required = True

        self.fields["is_active"].widget = forms.CheckboxInput()

        for field_name, field in self.fields.items():
            if field_name == "profile_picture":
                field.widget.attrs.update({
                    "class": "form-control"
                })
            elif field_name == "is_active":
                field.widget.attrs.update({
                    "class": "form-check-input"
                })
            else:
                field.widget.attrs.update({
                    "class": "form-control form-control-lg"
                })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "student"
        if commit:
            user.save()
        return user
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email
    
# --------------------------------------------------------------


class StudentUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        required=False
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "phone",
            "date_of_birth",
            "gender",
            "profile_picture",
            "is_active",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name == "profile_picture":
                field.widget = forms.FileInput(attrs={"class": "form-control"})
            elif field_name == "is_active":
                field.widget = forms.CheckboxInput(attrs={"class": "form-check-input"})
            else:
                field.widget.attrs.update({
                    "class": "form-control form-control-lg"
                })
