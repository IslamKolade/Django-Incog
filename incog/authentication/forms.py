from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from authentication.models import Profile, LoginAttempt
from django.contrib.auth.password_validation import validate_password
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    RegexValidator,
)
from django.utils import timezone


def ForbiddenUsers(value):
    forbidden_users = [
        "admin",
        "css",
        "css3",
        "js",
        "javascript",
        "auth",
        "authenticate",
        "login",
        "logout",
        "administrator",
        "root",
        "email",
        "user",
        "join",
        "sql",
        "static",
        "python",
        "delete",
        "password",
    ]
    if value.lower() in forbidden_users:
        raise ValidationError("Invalid username, this is a reserved word.")


def InvalidUser(value):
    if (
        "@" in value
        or "+" in value
        or "-" in value
        or "&" in value
        or " " in value
        or "\0" in value
    ):
        raise ValidationError(
            "Invalid username, do not include spaces or use these chars: @, -, +, &, ="
        )


def UniqueEmail(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError(f"User with this email already exists.")


def UniqueUser(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError("User with this username already exists.")


class LoginForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        # Check for too many failed login attempts
        if (
            LoginAttempt.objects.filter(
                timestamp__gt=timezone.now() - timezone.timedelta(minutes=10)
            ).count()
            > 10
        ):
            raise forms.ValidationError(
                "Too many failed login attempts. Please try again after 10 minutes."
            )
        return self.cleaned_data


class SignupForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(),
        error_messages={
            "required": "Please enter a username",
            "invalid": "Invalid username, do not include spaces or use these chars: @, -, +, &, =",
        },
        max_length=17,
        required=True,
    )
    email = forms.EmailField(
        max_length=100,
        required=False,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        validators=[
            MinLengthValidator(8),
            MaxLengthValidator(128),
            validate_password,
            RegexValidator(
                regex = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*_?&^])(?!.*[<>;\'\"\#])[A-Za-z\d@$!%*_?&^]{8,}$",
                message="Password must contain at least 1 letter, 1 number, and 1 special character",
            ),
        ],
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(), required=True, label="Confirm your password."
    )

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields["username"].validators.append(ForbiddenUsers)
        self.fields["username"].validators.append(InvalidUser)
        self.fields["username"].validators.append(UniqueUser)
        self.fields["email"].validators.append(UniqueEmail)

    def clean(self):
        super(SignupForm, self).clean()
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password != confirm_password:
            self._errors["confirm_password"] = self.error_class(
                ["Passwords do not match. Try again."]
            )
        if len(username) < 4:
            self._errors["username"] = self.error_class(
                ["Username must be more than 4 characters."]
            )
        if len(username) > 32:
            self._errors["username"] = self.error_class(
                ["Username must not be more than 16 characters."]
            )
        return self.cleaned_data


class ChangePasswordForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(
        widget=forms.PasswordInput(), label="Old password", required=True
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(), label="New password", required=True
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(), label="Confirm new password", required=True
    )

    class Meta:
        model = User
        fields = ("id", "old_password", "new_password", "confirm_password")

    def clean(self):
        super(ChangePasswordForm, self).clean()
        id = self.cleaned_data.get("id")
        old_password = self.cleaned_data.get("old_password")
        new_password = self.cleaned_data.get("new_password")
        confirm_password = self.cleaned_data.get("confirm_password")
        user = User.objects.get(pk=id)
        if not user.check_password(old_password):
            self._errors["old_password"] = self.error_class(
                ["Old password does not match."]
            )
        if new_password != confirm_password:
            self._errors["new_password"] = self.error_class(["Passwords do not match."])
        return self.cleaned_data


class EditProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)
    facebook_url = forms.URLField(
        widget=forms.TextInput(),
        required=False,
        max_length=100,
    )
    instagram_username = forms.CharField(
        widget=forms.TextInput(),
        required=False,
        max_length=50,
    )
    twitter_username = forms.CharField(
        widget=forms.TextInput(),
        required=False,
        max_length=50,
    )
    whatsapp_number = forms.CharField(
        widget=forms.TextInput(),
        required=False,
        max_length=25,
    )
    bio = forms.CharField(widget=forms.TextInput(), max_length=160, required=False)

    class Meta:
        model = Profile
        fields = (
            "profile_picture",
            "facebook_url",
            "instagram_username",
            "twitter_username",
            "whatsapp_number",
            "bio",
        )
