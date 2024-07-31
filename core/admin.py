from django.contrib import admin

from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'country', 'city', 'date_created')
    list_filter = ('country', 'city', 'date_created', 'date_updated')
    search_fields = ('user__username', 'full_name', 'phone', 'country', 'city')
    readonly_fields = ('date_created', 'date_updated')

admin.site.register(Profile, ProfileAdmin)
