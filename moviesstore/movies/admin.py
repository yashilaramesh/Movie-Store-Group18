from django.contrib import admin
from accounts.models import CustomUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import Movie, Review


class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('security_question_1', 'security_answer_1', 'security_question_2', 'security_answer_2')}),
    )

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)

admin.site.register(CustomUser, CustomUserAdmin)