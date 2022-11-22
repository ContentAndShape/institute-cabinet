from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User, Course, Institute, Student, Teacher

# TODO Make all UserCreationForm fields display on admin registration page
class UserCreationForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password1 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    type = forms.RadioSelect(choices=('student', 'teacher'))

    class Meta:
        model = User
        fields = ('email', 'type')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if (password1 and password2) and (password1 != password2):
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.type = self.type
        user.first_name = self.first_name
        user.last_name = self.last_name
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'type', 'is_active', 'is_admin')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    form_add = UserCreationForm

    list_display = ('email', 'type', 'first_name', 'last_name', 'is_admin')
    list_filter = ('is_admin', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('last_name',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(Course)
admin.site.register(Institute)
admin.site.register(Student)
admin.site.register(Teacher)
