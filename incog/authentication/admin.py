from django.contrib import admin
from authentication.models import Profile, LoginAttempt
# Register your models here.

admin.site.register(Profile)
admin.site.register(LoginAttempt)