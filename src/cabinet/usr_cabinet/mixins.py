from django.db import models

class UserReprMixin():

    class Meta:
        abstract = True
        ordering = ['last_name']

    def __str__(self) -> str:
        return self.get_full_name()


class NameMixin(models.Model):
    '''Used for naming inanimate entities'''
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class UserIdMixin(models.Model):
    user = models.OneToOneField(
        'User',
        on_delete=models.CASCADE,
        unique=True,
        primary_key=True,
    )

    class Meta:
        abstract = True
